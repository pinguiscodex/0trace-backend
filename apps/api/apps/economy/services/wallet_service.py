from decimal import Decimal

from django.db import transaction

from apps.common.api.errors import GameAPIException
from apps.common.services.ids import short_code
from apps.economy.models import CoinDefinition, Wallet, WalletBalance


def bootstrap_starter_wallet(user):
    wallet, _ = Wallet.objects.get_or_create(owner=user, label="Starter Wallet", defaults={"address": short_code("ztw_")})
    credits = CoinDefinition.objects.get(slug="credits")
    WalletBalance.objects.get_or_create(wallet=wallet, coin=credits, defaults={"amount": Decimal("1000.00")})
    for coin in CoinDefinition.objects.filter(is_primary=False):
        WalletBalance.objects.get_or_create(wallet=wallet, coin=coin, defaults={"amount": Decimal("0")})
    return wallet


def create_wallet(*, user, label: str):
    return Wallet.objects.create(owner=user, label=label, address=short_code("ztw_"))


@transaction.atomic
def delete_wallet(*, user, wallet: Wallet):
    wallet = Wallet.objects.select_for_update().get(id=wallet.id, owner=user)
    if wallet.balances.filter(amount__gt=0).exists():
        raise GameAPIException("Wallet still has a balance.", code="conflict", status_code=409)
    wallet.active = False
    wallet.save(update_fields=["active", "updated_at"])
    return wallet

