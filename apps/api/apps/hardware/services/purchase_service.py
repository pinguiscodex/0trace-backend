from decimal import Decimal
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.common.api.errors import GameAPIException
from apps.hardware.models import Delivery, DeliverySubscription, HardwareItem, HardwareCatalogItem
from apps.economy.models import CoinDefinition, Wallet, WalletBalance, WalletTransaction
from apps.telemetry.services.audit_log_service import audit


def _get_wallet_balance(wallet, coin):
    """Get or create wallet balance for a coin, with row lock."""
    balance, _ = WalletBalance.objects.select_for_update().get_or_create(
        wallet=wallet, coin=coin, defaults={"amount": Decimal("0")}
    )
    return balance


@transaction.atomic
def purchase_hardware(
    *, user, catalog_item: HardwareCatalogItem, machine=None, target_machine_id=None, request=None
):
    """
    Purchase hardware from the catalog.

    Args:
        user: The user making the purchase
        catalog_item: The catalog item to purchase
        machine: (deprecated) The active machine for delivery target
        target_machine_id: The machine to deliver to (optional, defaults to active machine)
        request: HTTP request object for audit logging

    Returns:
        The created Delivery object

    Raises:
        GameAPIException: If user lacks funds, item is unavailable, or machine not found
    """
    if not catalog_item:
        raise GameAPIException("Catalog item not found.", code="not_found", status_code=404)

    if catalog_item.price <= 0:
        raise GameAPIException("Item cannot be purchased.", code="validation_error")

    # Get primary wallet (first wallet for the user, locked for update)
    try:
        wallet = Wallet.objects.select_for_update().filter(owner=user, active=True).first()
        if not wallet:
            raise GameAPIException(
                "You do not have an active wallet.",
                code="wallet_not_found",
                status_code=409,
            )
    except Wallet.DoesNotExist:
        raise GameAPIException(
            "You do not have an active wallet.",
            code="wallet_not_found",
            status_code=409,
        )

    # Get credits coin
    try:
        credits = CoinDefinition.objects.get(slug="credits")
    except CoinDefinition.DoesNotExist:
        raise GameAPIException(
            "Credits currency not available.",
            code="system_error",
            status_code=500,
        )

    # Check balance
    balance = _get_wallet_balance(wallet, credits)
    price = Decimal(str(catalog_item.price))

    if balance.amount < price:
        raise GameAPIException(
            "Not enough credits to purchase this item.",
            code="not_enough_funds",
            status_code=409,
            details={"required": str(price), "available": str(balance.amount)},
        )

    # Deduct credits atomically
    balance.amount -= price
    balance.save(update_fields=["amount", "updated_at"])

    # Create hardware item
    item = HardwareItem.objects.create(
        owner=user,
        catalog_item=catalog_item,
        serial_number=f"{catalog_item.sku}-{timezone.now().timestamp():.0f}",
        status=HardwareItem.Status.DELIVERING,
    )

    WalletTransaction.objects.create(
        kind="hardware_purchase",
        from_wallet=wallet,
        coin=credits,
        amount=price,
        metadata={"catalog_item": catalog_item.sku},
    )

    # Determine delivery speed and ETA
    subscription = DeliverySubscription.objects.filter(user=user).first()
    has_express = subscription and subscription.active and subscription.expires_at and subscription.expires_at > timezone.now()
    speed = "express" if has_express else "normal"
    eta = timezone.now() + timedelta(minutes=20 if has_express else 120)

    # Create delivery
    delivery = Delivery.objects.create(
        owner=user,
        machine=machine,  # May be None if not specified
        catalog_item=catalog_item,
        hardware_item=item,
        status=Delivery.Status.PENDING,
        eta=eta,
        speed=speed,
        quantity=1,
    )

    # Audit the purchase
    audit(
        actor=user,
        event_type="hardware_purchase",
        request=request,
        metadata={
            "catalog_item": str(catalog_item.id),
            "price": str(price),
            "delivery": str(delivery.id),
        },
    )

    return delivery
