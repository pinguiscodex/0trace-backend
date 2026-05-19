from decimal import Decimal
from datetime import timedelta

import pytest
from django.utils import timezone

from apps.accounts.models import User
from apps.economy.models import CoinDefinition, WalletBalance, WalletTransaction
from apps.hardware.models import HardwareCatalogItem, HardwareItem, InventoryItem
from apps.hardware.services.delivery_service import claim_delivery
from apps.hardware.services.purchase_service import purchase_hardware
from apps.machines.services.machine_bootstrap_service import bootstrap_machine_for_user


@pytest.mark.django_db
def test_hardware_purchase_debits_credits_and_claim_places_item_in_inventory(seeded):
    user = User.objects.create_user("buyer", "buyer@example.com", "correct horse battery", display_name="Buyer")
    machine = bootstrap_machine_for_user(user)
    catalog = HardwareCatalogItem.objects.get(sku="starter-cpu")
    credits = CoinDefinition.objects.get(slug="credits")
    wallet = user.wallets.get(label="Starter Wallet")
    balance = WalletBalance.objects.get(wallet=wallet, coin=credits)
    starting_amount = balance.amount

    delivery = purchase_hardware(user=user, catalog_item=catalog, machine=machine)

    balance.refresh_from_db()
    assert balance.amount == starting_amount - Decimal("25.00")
    assert delivery.hardware_item.status == HardwareItem.Status.DELIVERING
    assert WalletTransaction.objects.filter(kind="hardware_purchase", from_wallet=wallet, amount=Decimal("25.00")).exists()

    delivery.eta = timezone.now() - timedelta(seconds=1)
    delivery.save(update_fields=["eta", "updated_at"])
    claimed = claim_delivery(user=user, delivery=delivery)

    claimed.hardware_item.refresh_from_db()
    assert claimed.status == delivery.Status.CLAIMED
    assert claimed.hardware_item.status == HardwareItem.Status.INVENTORY
    assert InventoryItem.objects.filter(machine=machine, item=claimed.hardware_item).exists()
