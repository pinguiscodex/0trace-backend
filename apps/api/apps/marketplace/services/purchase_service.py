from decimal import Decimal

from django.db import transaction

from apps.common.api.errors import GameAPIException
from apps.economy.models import Wallet, WalletBalance, WalletTransaction
from apps.hardware.models import HardwareItem, InventoryItem
from apps.marketplace.models import MarketplaceListing, MarketplaceTransaction
from apps.telemetry.services.audit_log_service import audit


@transaction.atomic
def purchase_listing(*, buyer, listing: MarketplaceListing, buyer_wallet_id, seller_wallet_id=None, idempotency_key: str | None = None, request=None):
    if idempotency_key:
        existing = MarketplaceTransaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing
    listing = MarketplaceListing.objects.select_for_update().get(id=listing.id)
    if listing.status != MarketplaceListing.Status.ACTIVE:
        raise GameAPIException("Listing is already sold or unavailable.", code="listing_already_sold", status_code=409)
    if listing.seller_id == buyer.id:
        raise GameAPIException("Cannot buy your own listing.", code="permission_denied", status_code=403)
    buyer_wallet = Wallet.objects.select_for_update().get(id=buyer_wallet_id, owner=buyer, active=True)
    seller_wallet = Wallet.objects.select_for_update().filter(owner=listing.seller, active=True).first()
    if seller_wallet_id:
        seller_wallet = Wallet.objects.select_for_update().get(id=seller_wallet_id, owner=listing.seller, active=True)
    if seller_wallet is None:
        raise GameAPIException("Seller has no wallet.", code="conflict", status_code=409)
    debit, _ = WalletBalance.objects.select_for_update().get_or_create(wallet=buyer_wallet, coin=listing.coin, defaults={"amount": Decimal("0")})
    credit, _ = WalletBalance.objects.select_for_update().get_or_create(wallet=seller_wallet, coin=listing.coin, defaults={"amount": Decimal("0")})
    if debit.amount < listing.price:
        raise GameAPIException("Not enough credits to complete this purchase.", code="not_enough_funds", status_code=409, details={"required": str(listing.price), "available": str(debit.amount)})
    debit.amount -= listing.price
    credit.amount += listing.price
    debit.save(update_fields=["amount", "updated_at"])
    credit.save(update_fields=["amount", "updated_at"])
    listing.status = MarketplaceListing.Status.SOLD
    listing.buyer = buyer
    listing.save(update_fields=["status", "buyer", "updated_at"])
    if listing.hardware_item_id:
        item = listing.hardware_item
        item.owner = buyer
        item.status = HardwareItem.Status.INVENTORY
        item.save(update_fields=["owner", "status", "updated_at"])
        machine = buyer.machines.filter(active=True).first()
        if machine:
            InventoryItem.objects.update_or_create(machine=machine, item=item, defaults={"status": "available"})
    if listing.software_file_id:
        software = listing.software_file
        software.owner = buyer
        software.machine = buyer.machines.filter(active=True).first() or software.machine
        software.save(update_fields=["owner", "machine", "updated_at"])
    WalletTransaction.objects.create(kind="marketplace_purchase", from_wallet=buyer_wallet, to_wallet=seller_wallet, coin=listing.coin, amount=listing.price, metadata={"listing": str(listing.id)})
    tx = MarketplaceTransaction.objects.create(listing=listing, buyer=buyer, seller=listing.seller, price=listing.price, coin=listing.coin, idempotency_key=idempotency_key)
    audit(actor=buyer, event_type="marketplace_purchase", request=request, metadata={"listing": str(listing.id), "transaction": str(tx.id)})
    return tx

