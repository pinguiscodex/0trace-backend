from apps.common.services.ids import short_code
from apps.hardware.models import HardwareCatalogItem, HardwareItem, InventoryItem


STARTER_HARDWARE = ["starter-cpu", "starter-motherboard", "starter-ram", "starter-ssd", "starter-case"]


def bootstrap_starter_hardware(machine):
    for sku in STARTER_HARDWARE:
        catalog = HardwareCatalogItem.objects.filter(sku=sku).first()
        if catalog is None:
            continue
        item, _ = HardwareItem.objects.get_or_create(
            owner=machine.owner,
            catalog_item=catalog,
            serial_number=f"{sku}-{machine.id.hex[:8]}",
            defaults={"status": HardwareItem.Status.INVENTORY},
        )
        InventoryItem.objects.get_or_create(machine=machine, item=item)

