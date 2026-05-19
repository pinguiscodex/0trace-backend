from .models import HardwareCatalogItem


def catalog_items():
    return HardwareCatalogItem.objects.all()

