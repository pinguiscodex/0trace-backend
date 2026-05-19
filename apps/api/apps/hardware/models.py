from django.conf import settings
from django.db import models

from apps.common.models.base import UUIDModel


class HardwareCatalogItem(UUIDModel):
    class Category(models.TextChoices):
        CPU = "cpu", "CPU"
        GPU = "gpu", "GPU"
        MOTHERBOARD = "motherboard", "Motherboard"
        RAM = "ram", "RAM"
        HDD = "hdd", "HDD"
        SSD = "ssd", "SSD"
        USB = "usb", "USB Stick"
        CASE = "case", "Case"
        PEAR_CHIP = "pear_chip", "Integrated Pear Chip"

    sku = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=40, choices=Category.choices)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    stats = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["category", "price"])]
        ordering = ["category", "price", "name"]

    def __str__(self) -> str:
        return self.name


class HardwareItem(UUIDModel):
    class Status(models.TextChoices):
        INVENTORY = "inventory", "Inventory"
        EQUIPPED = "equipped", "Equipped"
        LISTED = "listed", "Listed"
        DELIVERING = "delivering", "Delivering"
        SOLD = "sold", "Sold"
        TRASH = "trash", "Trash"

    catalog_item = models.ForeignKey(HardwareCatalogItem, on_delete=models.PROTECT, related_name="items")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hardware_items")
    serial_number = models.CharField(max_length=80, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INVENTORY)

    class Meta:
        indexes = [models.Index(fields=["owner", "status"])]


class InventoryItem(UUIDModel):
    machine = models.ForeignKey("machines.Machine", on_delete=models.CASCADE, related_name="inventory_items")
    item = models.OneToOneField(HardwareItem, on_delete=models.CASCADE, related_name="inventory_record")
    status = models.CharField(max_length=20, default="available", db_index=True)

    class Meta:
        indexes = [models.Index(fields=["machine", "status"])]


class EquippedHardware(UUIDModel):
    machine = models.ForeignKey("machines.Machine", on_delete=models.CASCADE, related_name="equipped_hardware")
    item = models.OneToOneField(HardwareItem, on_delete=models.CASCADE, related_name="equipment_record")
    slot = models.CharField(max_length=60)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["machine", "slot"], name="unique_equipped_slot_per_machine")]
        indexes = [models.Index(fields=["machine", "slot"])]


class Delivery(UUIDModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_TRANSIT = "in_transit", "In Transit"
        DELIVERED = "delivered", "Delivered"
        CLAIMED = "claimed", "Claimed"
        CANCELLED = "cancelled", "Cancelled"
        FAILED = "failed", "Failed"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="deliveries")
    machine = models.ForeignKey("machines.Machine", null=True, blank=True, on_delete=models.SET_NULL, related_name="deliveries")
    catalog_item = models.ForeignKey(HardwareCatalogItem, null=True, blank=True, on_delete=models.PROTECT, related_name="deliveries")
    hardware_item = models.OneToOneField(HardwareItem, null=True, blank=True, on_delete=models.SET_NULL, related_name="delivery")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    eta = models.DateTimeField()
    delivered_at = models.DateTimeField(null=True, blank=True)
    claimed_at = models.DateTimeField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    speed = models.CharField(max_length=20, default="normal")
    idempotency_key = models.CharField(max_length=120, null=True, blank=True, unique=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["owner", "status", "eta"])]


class DeliverySubscription(UUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="delivery_subscription")
    active = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)

