from django.urls import path

from .views import MarketplaceListingCancelView, MarketplaceListingDetailView, MarketplaceListingListCreateView, MarketplaceListingPurchaseView

urlpatterns = [
    path("marketplace/listings/", MarketplaceListingListCreateView.as_view(), name="marketplace-listings"),
    path("marketplace/listings/<uuid:listing_id>/", MarketplaceListingDetailView.as_view(), name="marketplace-listing-detail"),
    path("marketplace/listings/<uuid:listing_id>/cancel/", MarketplaceListingCancelView.as_view(), name="marketplace-listing-cancel"),
    path("marketplace/listings/<uuid:listing_id>/purchase/", MarketplaceListingPurchaseView.as_view(), name="marketplace-listing-purchase"),
]

