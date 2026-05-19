from django.contrib import admin

from .models import CoinDefinition, CoinPricePoint, MiningJob, Wallet, WalletBalance, WalletTransaction


admin.site.register(CoinDefinition)
admin.site.register(CoinPricePoint)
admin.site.register(Wallet)
admin.site.register(WalletBalance)
admin.site.register(WalletTransaction)
admin.site.register(MiningJob)

