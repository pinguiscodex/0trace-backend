from django.db import transaction
from django.utils import timezone

from apps.common.api.errors import GameAPIException
from apps.hardware.models import Delivery, HardwareItem, InventoryItem
from apps.telemetry.services.audit_log_service import audit


@transaction.atomic
def claim_delivery(*, user, delivery: Delivery, request=None):
    delivery = Delivery.objects.select_for_update().get(id=delivery.id)
    if delivery.owner_id != user.id:
        raise GameAPIException("Delivery not found.", code="not_found", status_code=404)
    if delivery.status == Delivery.Status.CLAIMED:
        return delivery
    if delivery.status not in {Delivery.Status.DELIVERED, Delivery.Status.IN_TRANSIT, Delivery.Status.PENDING}:
        raise GameAPIException("Delivery cannot be claimed.", code="conflict", status_code=409)
    if delivery.eta > timezone.now():
        raise GameAPIException("Delivery has not arrived.", code="conflict", status_code=409)
    if delivery.hardware_item_id is None and delivery.catalog_item_id:
        item = HardwareItem.objects.create(
            owner=user,
            catalog_item=delivery.catalog_item,
            serial_number=f"{delivery.catalog_item.sku}-{delivery.id.hex[:10]}",
            status=HardwareItem.Status.INVENTORY,
        )
        delivery.hardware_item = item
    if delivery.hardware_item_id:
        delivery.hardware_item.status = HardwareItem.Status.INVENTORY
        delivery.hardware_item.save(update_fields=["status", "updated_at"])
    if delivery.machine_id and delivery.hardware_item_id:
        InventoryItem.objects.get_or_create(machine=delivery.machine, item=delivery.hardware_item)
    delivery.status = Delivery.Status.CLAIMED
    delivery.delivered_at = delivery.delivered_at or timezone.now()
    delivery.claimed_at = timezone.now()
    delivery.save()
    audit(actor=user, event_type="delivery_claim", request=request, metadata={"delivery": str(delivery.id)})
    return delivery
