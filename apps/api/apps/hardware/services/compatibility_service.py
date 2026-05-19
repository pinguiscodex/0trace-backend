from apps.common.api.errors import GameAPIException


def validate_equipment(machine, item, slot: str):
    catalog = item.catalog_item
    if item.owner_id != machine.owner_id:
        raise GameAPIException("Hardware not found.", code="not_found", status_code=404)
    if item.status not in {"inventory", "equipped"}:
        raise GameAPIException("Hardware is not available.", code="conflict", status_code=409)
    if machine.equipped_hardware.filter(slot=slot).exclude(item=item).exists():
        raise GameAPIException("No free slot is available.", code="hardware_incompatible", status_code=409)
    if catalog.category == "gpu" and machine.equipped_hardware.filter(item__catalog_item__category="pear_chip").exists():
        raise GameAPIException("Pear chip systems cannot equip GPUs.", code="hardware_incompatible", status_code=409)
    if catalog.category == "pear_chip" and machine.equipped_hardware.filter(item__catalog_item__category="gpu").exists():
        raise GameAPIException("Pear chip systems cannot use GPUs.", code="hardware_incompatible", status_code=409)

