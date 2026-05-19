from decimal import Decimal

import pytest

from apps.accounts.models import User
from apps.economy.models import CoinDefinition, Wallet, WalletBalance
from apps.economy.services.transfer_service import transfer
from apps.economy.services.wallet_service import bootstrap_starter_wallet
from apps.hardware.models import HardwareCatalogItem, HardwareItem
from apps.marketplace.services.listing_service import create_listing
from apps.marketplace.services.purchase_service import purchase_listing


@pytest.mark.django_db(transaction=True)
def test_wallet_transfer_prevents_double_spend(seeded):
    sender = User.objects.create_user("sender", "sender@example.com", "correct horse battery", display_name="Sender")
    receiver = User.objects.create_user("receiver", "receiver@example.com", "correct horse battery", display_name="Receiver")
    sender_wallet = bootstrap_starter_wallet(sender)
    receiver_wallet = bootstrap_starter_wallet(receiver)
    coin = CoinDefinition.objects.get(slug="credits")
    WalletBalance.objects.filter(wallet=sender_wallet, coin=coin).update(amount=Decimal("10.00"))

    with pytest.raises(Exception):
        transfer(user=sender, from_wallet=sender_wallet, to_address=receiver_wallet.address, coin_slug="credits", amount=Decimal("11.00"))

    assert WalletBalance.objects.get(wallet=sender_wallet, coin=coin).amount == Decimal("10.00000000")


@pytest.mark.django_db(transaction=True)
def test_marketplace_purchase_marks_listing_sold_and_rejects_second_buyer(seeded):
    seller = User.objects.create_user("seller", "seller@example.com", "correct horse battery", display_name="Seller")
    buyer = User.objects.create_user("buyer", "buyer@example.com", "correct horse battery", display_name="Buyer")
    other = User.objects.create_user("other", "other@example.com", "correct horse battery", display_name="Other")
    seller_wallet = bootstrap_starter_wallet(seller)
    buyer_wallet = bootstrap_starter_wallet(buyer)
    other_wallet = bootstrap_starter_wallet(other)
    coin = CoinDefinition.objects.get(slug="credits")
    WalletBalance.objects.filter(wallet=buyer_wallet, coin=coin).update(amount=Decimal("100.00"))
    WalletBalance.objects.filter(wallet=other_wallet, coin=coin).update(amount=Decimal("100.00"))
    catalog = HardwareCatalogItem.objects.get(sku="starter-cpu")
    item = HardwareItem.objects.create(owner=seller, catalog_item=catalog, serial_number="cpu-race-test")
    listing = create_listing(user=seller, item_type="hardware", item_id=item.id, title="CPU", description="", price=Decimal("25.00"))

    tx = purchase_listing(buyer=buyer, listing=listing, buyer_wallet_id=buyer_wallet.id)

    assert tx.status == "succeeded"
    listing.refresh_from_db()
    assert listing.status == "sold"
    assert listing.buyer == buyer
    with pytest.raises(Exception):
        purchase_listing(buyer=other, listing=listing, buyer_wallet_id=other_wallet.id)
    item.refresh_from_db()
    assert item.owner == buyer

