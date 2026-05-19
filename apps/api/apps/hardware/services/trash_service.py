from django.db import transaction

from apps.hardware.models import HardwareItem, InventoryItem, EquippedHardware
from apps.telemetry.services.audit_log_service import audit


@transaction.atomic
def move_to_trash(*, user, hardware_item_id, request=None):
    item = HardwareItem.objects.select_for_update().get(id=hardware_item_id, owner=user)
    if item.status == HardwareItem.Status.EQUIPPED:
        EquippedHardware.objects.filter(item=item).delete()
    InventoryItem.objects.filter(item=item).delete()
    item.status = HardwareItem.Status.TRASH
    item.save(update_fields=["status", "updated_at"])
    audit(actor=user, event_type="hardware_trash", request=request, metadata={"item": str(item.id)})
    return item


@transaction.atomic
def restore_from_trash(*, user, hardware_item_id, request=None):
    item = HardwareItem.objects.select_for_update().get(id=hardware_item_id, owner=user, status=HardwareItem.Status.TRASH)
    item.status = HardwareItem.Status.INVENTORY
    item.save(update_fields=["status", "updated_at"])
    audit(actor=user, event_type="hardware_restore", request=request, metadata={"item": str(item.id)})
    return item


@transaction.atomic
def delete_permanently(*, user, hardware_item_id, request=None):
    item = HardwareItem.objects.select_for_update().get(id=hardware_item_id, owner=user, status=HardwareItem.Status.TRASH)
    item_id = str(item.id)
    item.delete()
    audit(actor=user, event_type="hardware_delete", request=request, metadata={"item": item_id})
    return item_id
