from decimal import Decimal

from django.db import transaction

from apps.common.api.errors import GameAPIException
from apps.economy.models import CoinDefinition, Wallet, WalletBalance, WalletTransaction
from apps.economy.services.coin_price_service import latest_price
from apps.telemetry.services.audit_log_service import audit


def _balance(wallet, coin):
    balance, _ = WalletBalance.objects.select_for_update().get_or_create(wallet=wallet, coin=coin, defaults={"amount": Decimal("0")})
    return balance


@transaction.atomic
def transfer(*, user, from_wallet: Wallet, to_address: str, coin_slug: str, amount: Decimal, idempotency_key: str | None = None, request=None):
    if idempotency_key:
        existing = WalletTransaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing
    if amount <= 0:
        raise GameAPIException("Amount must be positive.", code="validation_error")
    from_wallet = Wallet.objects.select_for_update().get(id=from_wallet.id, owner=user, active=True)
    to_wallet = Wallet.objects.select_for_update().get(address=to_address, active=True)
    coin = CoinDefinition.objects.get(slug=coin_slug)
    debit = _balance(from_wallet, coin)
    credit = _balance(to_wallet, coin)
    if debit.amount < amount:
        raise GameAPIException(
            "Not enough credits to complete this transfer.",
            code="not_enough_funds",
            status_code=409,
            details={"required": str(amount), "available": str(debit.amount)},
        )
    debit.amount -= amount
    credit.amount += amount
    debit.save(update_fields=["amount", "updated_at"])
    credit.save(update_fields=["amount", "updated_at"])
    tx = WalletTransaction.objects.create(
        kind="transfer",
        from_wallet=from_wallet,
        to_wallet=to_wallet,
        coin=coin,
        amount=amount,
        idempotency_key=idempotency_key,
    )
    audit(actor=user, event_type="wallet_transfer", request=request, metadata={"transaction": str(tx.id)})
    return tx


@transaction.atomic
def buy_coin(*, user, wallet: Wallet, coin_slug: str, credit_amount: Decimal, request=None):
    if credit_amount <= 0:
        raise GameAPIException("Amount must be positive.", code="validation_error")
    wallet = Wallet.objects.select_for_update().get(id=wallet.id, owner=user, active=True)
    credits = CoinDefinition.objects.get(slug="credits")
    coin = CoinDefinition.objects.get(slug=coin_slug)
    if coin.slug == "credits":
        raise GameAPIException("Cannot buy credits with credits.", code="validation_error")
    price = latest_price(coin)
    if price is None:
        raise GameAPIException("Coin has no price.", code="conflict", status_code=409)
    credits_balance = _balance(wallet, credits)
    coin_balance = _balance(wallet, coin)
    if credits_balance.amount < credit_amount:
        raise GameAPIException("Not enough credits to complete this purchase.", code="not_enough_funds", status_code=409, details={"required": str(credit_amount), "available": str(credits_balance.amount)})
    coin_amount = (credit_amount / price.price_credits).quantize(Decimal("0.00000001"))
    credits_balance.amount -= credit_amount
    coin_balance.amount += coin_amount
    credits_balance.save(update_fields=["amount", "updated_at"])
    coin_balance.save(update_fields=["amount", "updated_at"])
    tx = WalletTransaction.objects.create(kind="coin_buy", from_wallet=wallet, to_wallet=wallet, coin=coin, amount=coin_amount, metadata={"credit_amount": str(credit_amount), "price": str(price.price_credits)})
    audit(actor=user, event_type="coin_buy", request=request, metadata={"transaction": str(tx.id)})
    return tx


@transaction.atomic
def sell_coin(*, user, wallet: Wallet, coin_slug: str, coin_amount: Decimal, request=None):
    if coin_amount <= 0:
        raise GameAPIException("Amount must be positive.", code="validation_error")
    wallet = Wallet.objects.select_for_update().get(id=wallet.id, owner=user, active=True)
    credits = CoinDefinition.objects.get(slug="credits")
    coin = CoinDefinition.objects.get(slug=coin_slug)
    if coin.slug == "credits":
        raise GameAPIException("Cannot sell credits for credits.", code="validation_error")
    price = latest_price(coin)
    if price is None:
        raise GameAPIException("Coin has no price.", code="conflict", status_code=409)
    coin_balance = _balance(wallet, coin)
    credits_balance = _balance(wallet, credits)
    if coin_balance.amount < coin_amount:
        raise GameAPIException("Not enough coin balance to sell.", code="not_enough_funds", status_code=409, details={"required": str(coin_amount), "available": str(coin_balance.amount)})
    credit_amount = (coin_amount * price.price_credits).quantize(Decimal("0.00000001"))
    coin_balance.amount -= coin_amount
    credits_balance.amount += credit_amount
    coin_balance.save(update_fields=["amount", "updated_at"])
    credits_balance.save(update_fields=["amount", "updated_at"])
    tx = WalletTransaction.objects.create(kind="coin_sell", from_wallet=wallet, to_wallet=wallet, coin=coin, amount=coin_amount, metadata={"credit_amount": str(credit_amount), "price": str(price.price_credits)})
    audit(actor=user, event_type="coin_sell", request=request, metadata={"transaction": str(tx.id)})
    return tx
