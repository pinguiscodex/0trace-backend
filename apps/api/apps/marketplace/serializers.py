from rest_framework import serializers

from .models import MarketplaceListing, MarketplaceTransaction


class MarketplaceListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceListing
        fields = "__all__"


class MarketplaceListingCreateSerializer(serializers.Serializer):
    item_type = serializers.ChoiceField(choices=["software", "hardware"])
    item_id = serializers.UUIDField()
    title = serializers.CharField(max_length=160)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=18, decimal_places=8)
    coin_slug = serializers.SlugField(default="credits")


class MarketplacePurchaseSerializer(serializers.Serializer):
    buyer_wallet_id = serializers.UUIDField()
    idempotency_key = serializers.CharField(required=False, allow_blank=True)


class MarketplaceTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceTransaction
        fields = "__all__"

