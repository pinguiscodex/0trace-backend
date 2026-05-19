from .models import MarketplaceListing


def active_listings():
    return MarketplaceListing.objects.filter(status=MarketplaceListing.Status.ACTIVE)

