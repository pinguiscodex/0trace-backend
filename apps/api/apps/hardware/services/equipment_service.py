from django.db import transaction

from apps.hardware.models import EquippedHardware, HardwareItem, InventoryItem
from apps.hardware.services.compatibility_service import validate_equipment
from apps.telemetry.services.audit_log_service import audit


@transaction.atomic
def equip_item(*, user, machine, hardware_item_id, slot: str, request=None):
    item = HardwareItem.objects.select_for_update().get(id=hardware_item_id, owner=user)
    validate_equipment(machine, item, slot)
    EquippedHardware.objects.update_or_create(machine=machine, item=item, defaults={"slot": slot})
    item.status = HardwareItem.Status.EQUIPPED
    item.save(update_fields=["status", "updated_at"])
    InventoryItem.objects.filter(item=item).update(status="equipped")
    audit(actor=user, event_type="hardware_equip", request=request, metadata={"item": str(item.id), "slot": slot})
    return item


@transaction.atomic
def unequip_item(*, user, machine, hardware_item_id, request=None):
    item = HardwareItem.objects.select_for_update().get(id=hardware_item_id, owner=user)
    EquippedHardware.objects.filter(machine=machine, item=item).delete()
    item.status = HardwareItem.Status.INVENTORY
    item.save(update_fields=["status", "updated_at"])
    InventoryItem.objects.update_or_create(machine=machine, item=item, defaults={"status": "available"})
    audit(actor=user, event_type="hardware_unequip", request=request, metadata={"item": str(item.id)})
    return item

