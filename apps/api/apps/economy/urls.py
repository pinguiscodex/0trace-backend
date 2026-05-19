from django.urls import path

from .views import (
    CoinListView,
    CoinBuyView,
    CoinPricesView,
    CoinSellView,
    MiningJobCancelView,
    MiningJobDetailView,
    MiningJobListCreateView,
    WalletDetailView,
    WalletListCreateView,
    WalletTransferView,
)

urlpatterns = [
    path("coins/", CoinListView.as_view(), name="coins"),
    path("coins/<slug:slug>/prices/", CoinPricesView.as_view(), name="coin-prices"),
    path("coins/<slug:slug>/buy/", CoinBuyView.as_view(), name="coin-buy"),
    path("coins/<slug:slug>/sell/", CoinSellView.as_view(), name="coin-sell"),
    path("wallets/", WalletListCreateView.as_view(), name="wallets"),
    path("wallets/<uuid:wallet_id>/", WalletDetailView.as_view(), name="wallet-detail"),
    path("wallets/<uuid:wallet_id>/transfer/", WalletTransferView.as_view(), name="wallet-transfer"),
    path("mining-jobs/", MiningJobListCreateView.as_view(), name="mining-jobs"),
    path("mining-jobs/<uuid:mining_job_id>/", MiningJobDetailView.as_view(), name="mining-job-detail"),
    path("mining-jobs/<uuid:mining_job_id>/cancel/", MiningJobCancelView.as_view(), name="mining-job-cancel"),
]
