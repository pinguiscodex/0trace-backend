from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from apps.common.api.responses import ok

from .models import MarketplaceListing
from .serializers import MarketplaceListingCreateSerializer, MarketplaceListingSerializer, MarketplacePurchaseSerializer, MarketplaceTransactionSerializer
from .services.listing_service import cancel_listing, create_listing
from .services.purchase_service import purchase_listing


@extend_schema(tags=["marketplace"])
class MarketplaceListingListCreateView(APIView):
    serializer_class = MarketplaceListingCreateSerializer

    @extend_schema(operation_id="marketplace_listings_list", responses={200: MarketplaceListingSerializer(many=True)})
    def get(self, request):
        queryset = MarketplaceListing.objects.filter(status=MarketplaceListing.Status.ACTIVE)
        item_type = request.GET.get("type")
        if item_type:
            queryset = queryset.filter(item_type=item_type)
        return ok(MarketplaceListingSerializer(queryset, many=True).data)

    @extend_schema(request=MarketplaceListingCreateSerializer, responses={201: MarketplaceListingSerializer})
    def post(self, request):
        serializer = MarketplaceListingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return ok(MarketplaceListingSerializer(create_listing(user=request.user, **serializer.validated_data)).data, status_code=201)


@extend_schema(tags=["marketplace"])
class MarketplaceListingDetailView(APIView):
    serializer_class = MarketplaceListingSerializer

    @extend_schema(operation_id="marketplace_listings_retrieve", responses={200: MarketplaceListingSerializer})
    def get(self, request, listing_id):
        return ok(MarketplaceListingSerializer(MarketplaceListing.objects.get(id=listing_id)).data)

    def patch(self, request, listing_id):
        listing = MarketplaceListing.objects.get(id=listing_id, seller=request.user)
        for field in ["title", "description", "price"]:
            if field in request.data:
                setattr(listing, field, request.data[field])
        listing.save()
        return ok(MarketplaceListingSerializer(listing).data)


@extend_schema(tags=["marketplace"])
class MarketplaceListingCancelView(APIView):
    serializer_class = MarketplaceListingSerializer

    def post(self, request, listing_id):
        return ok(MarketplaceListingSerializer(cancel_listing(user=request.user, listing=MarketplaceListing.objects.get(id=listing_id, seller=request.user))).data)


@extend_schema(tags=["marketplace"])
class MarketplaceListingPurchaseView(APIView):
    serializer_class = MarketplacePurchaseSerializer

    @extend_schema(request=MarketplacePurchaseSerializer, responses={200: MarketplaceTransactionSerializer})
    def post(self, request, listing_id):
        serializer = MarketplacePurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tx = purchase_listing(buyer=request.user, listing=MarketplaceListing.objects.get(id=listing_id), request=request, **serializer.validated_data)
        return ok(MarketplaceTransactionSerializer(tx).data)
