from django.contrib import admin

from .models import MarketplaceListing, MarketplaceTransaction


admin.site.register(MarketplaceListing)
admin.site.register(MarketplaceTransaction)

