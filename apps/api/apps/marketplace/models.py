from django.conf import settings
from django.db import models

from apps.common.models.base import UUIDModel


class MarketplaceListing(UUIDModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        SOLD = "sold", "Sold"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="marketplace_listings")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="marketplace_purchases")
    item_type = models.CharField(max_length=30)
    software_file = models.ForeignKey("software.SoftwareFile", null=True, blank=True, on_delete=models.PROTECT, related_name="marketplace_listings")
    hardware_item = models.ForeignKey("hardware.HardwareItem", null=True, blank=True, on_delete=models.PROTECT, related_name="marketplace_listings")
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=18, decimal_places=8)
    coin = models.ForeignKey("economy.CoinDefinition", on_delete=models.PROTECT, related_name="marketplace_listings")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        indexes = [
            models.Index(fields=["status", "item_type", "price"]),
            models.Index(fields=["seller", "status"]),
            models.Index(fields=["buyer", "status"]),
        ]


class MarketplaceTransaction(UUIDModel):
    listing = models.OneToOneField(MarketplaceListing, on_delete=models.PROTECT, related_name="transaction")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="marketplace_transactions_as_buyer")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="marketplace_transactions_as_seller")
    price = models.DecimalField(max_digits=18, decimal_places=8)
    coin = models.ForeignKey("economy.CoinDefinition", on_delete=models.PROTECT)
    status = models.CharField(max_length=20, default="succeeded")
    idempotency_key = models.CharField(max_length=120, null=True, blank=True, unique=True)


