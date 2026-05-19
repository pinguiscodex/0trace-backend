from django.contrib import admin

from .models import (
    Delivery,
    DeliverySubscription,
    EquippedHardware,
    HardwareCatalogItem,
    HardwareItem,
    InventoryItem,
)


admin.site.register(HardwareCatalogItem)
admin.site.register(HardwareItem)
admin.site.register(InventoryItem)
admin.site.register(EquippedHardware)
admin.site.register(Delivery)
admin.site.register(DeliverySubscription)
