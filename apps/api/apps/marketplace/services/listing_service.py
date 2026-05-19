from django.db import transaction

from apps.common.api.errors import GameAPIException
from apps.economy.models import CoinDefinition
from apps.hardware.models import HardwareItem
from apps.marketplace.models import MarketplaceListing
from apps.software.models import SoftwareFile


@transaction.atomic
def create_listing(*, user, item_type: str, item_id, title: str, description: str, price, coin_slug: str = "credits"):
    coin = CoinDefinition.objects.get(slug=coin_slug)
    listing = MarketplaceListing(seller=user, item_type=item_type, title=title, description=description, price=price, coin=coin, status=MarketplaceListing.Status.ACTIVE)
    if item_type == "software":
        software = SoftwareFile.objects.get(id=item_id, owner=user)
        if software.locked_by_job_id:
            raise GameAPIException("Software is locked by an active job.", code="conflict", status_code=409)
        listing.software_file = software
    elif item_type == "hardware":
        hardware = HardwareItem.objects.get(id=item_id, owner=user)
        if hardware.status == HardwareItem.Status.EQUIPPED:
            raise GameAPIException("Cannot list equipped hardware.", code="conflict", status_code=409)
        hardware.status = HardwareItem.Status.LISTED
        hardware.save(update_fields=["status", "updated_at"])
        listing.hardware_item = hardware
    else:
        raise GameAPIException("Unsupported listing type.", code="validation_error")
    listing.save()
    return listing


@transaction.atomic
def cancel_listing(*, user, listing: MarketplaceListing):
    listing = MarketplaceListing.objects.select_for_update().get(id=listing.id, seller=user)
    if listing.status != MarketplaceListing.Status.ACTIVE:
        raise GameAPIException("Listing is not active.", code="conflict", status_code=409)
    listing.status = MarketplaceListing.Status.CANCELLED
    listing.save(update_fields=["status", "updated_at"])
    if listing.hardware_item_id:
        listing.hardware_item.status = HardwareItem.Status.INVENTORY
        listing.hardware_item.save(update_fields=["status", "updated_at"])
    return listing

