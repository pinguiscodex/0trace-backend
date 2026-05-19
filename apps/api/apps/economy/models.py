from django.conf import settings
from django.db import models

from apps.common.models.base import UUIDModel


class CoinDefinition(UUIDModel):
    slug = models.SlugField(max_length=60, unique=True)
    symbol = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)
    difficulty = models.DecimalField(max_digits=14, decimal_places=6, default=1)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return self.symbol


class CoinPricePoint(UUIDModel):
    coin = models.ForeignKey(CoinDefinition, on_delete=models.CASCADE, related_name="price_points")
    price_at = models.DateTimeField()
    price_credits = models.DecimalField(max_digits=18, decimal_places=8)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["coin", "price_at"], name="unique_coin_price_at")]
        indexes = [models.Index(fields=["coin", "price_at"])]


class Wallet(UUIDModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallets")
    machine = models.ForeignKey("machines.Machine", null=True, blank=True, on_delete=models.SET_NULL, related_name="wallets")
    address = models.CharField(max_length=80, unique=True)
    label = models.CharField(max_length=80)
    active = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["owner"]), models.Index(fields=["address"])]


class WalletBalance(UUIDModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="balances")
    coin = models.ForeignKey(CoinDefinition, on_delete=models.PROTECT, related_name="wallet_balances")
    amount = models.DecimalField(max_digits=24, decimal_places=8, default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["wallet", "coin"], name="unique_wallet_coin_balance")]


class WalletTransaction(UUIDModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"

    kind = models.CharField(max_length=40)
    from_wallet = models.ForeignKey(Wallet, null=True, blank=True, on_delete=models.PROTECT, related_name="outgoing_transactions")
    to_wallet = models.ForeignKey(Wallet, null=True, blank=True, on_delete=models.PROTECT, related_name="incoming_transactions")
    coin = models.ForeignKey(CoinDefinition, on_delete=models.PROTECT, related_name="transactions")
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUCCEEDED)
    idempotency_key = models.CharField(max_length=120, null=True, blank=True, unique=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["coin", "created_at"]), models.Index(fields=["status", "created_at"])]


class MiningJob(UUIDModel):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        PAUSED = "paused", "Paused"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mining_jobs")
    machine = models.ForeignKey("machines.Machine", on_delete=models.CASCADE, related_name="mining_jobs")
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="mining_jobs")
    coin = models.ForeignKey(CoinDefinition, on_delete=models.PROTECT, related_name="mining_jobs")
    miner_software = models.ForeignKey("software.SoftwareFile", null=True, blank=True, on_delete=models.PROTECT, related_name="mining_jobs")
    persisted_job = models.OneToOneField("jobs.PersistedJob", null=True, blank=True, on_delete=models.SET_NULL, related_name="mining_job")
    mode = models.CharField(max_length=20, default="cpu")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    total_payout = models.DecimalField(max_digits=24, decimal_places=8, default=0)
    payout_settled_until = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["machine", "status"]), models.Index(fields=["user", "status"])]

