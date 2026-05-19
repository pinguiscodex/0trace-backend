from .models import Wallet


def wallets_for_user(user):
    return Wallet.objects.filter(owner=user)

