from decimal import Decimal

from rest_framework import serializers

from .models import CoinDefinition, CoinPricePoint, MiningJob, Wallet, WalletBalance, WalletTransaction


class CoinDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinDefinition
        fields = "__all__"


class CoinPricePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinPricePoint
        fields = "__all__"


class WalletBalanceSerializer(serializers.ModelSerializer):
    coin = CoinDefinitionSerializer()

    class Meta:
        model = WalletBalance
        fields = ["coin", "amount"]


class WalletSerializer(serializers.ModelSerializer):
    balances = WalletBalanceSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ["id", "address", "label", "active", "balances", "created_at", "updated_at"]


class WalletCreateSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=80)


class WalletTransferSerializer(serializers.Serializer):
    to_address = serializers.CharField(max_length=80)
    coin_slug = serializers.SlugField(default="credits")
    amount = serializers.DecimalField(max_digits=24, decimal_places=8, min_value=Decimal("0.00000001"))
    idempotency_key = serializers.CharField(required=False, allow_blank=True)


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = "__all__"


class CoinBuySerializer(serializers.Serializer):
    wallet_id = serializers.UUIDField()
    credit_amount = serializers.DecimalField(max_digits=24, decimal_places=8, min_value=Decimal("0.00000001"))


class CoinSellSerializer(serializers.Serializer):
    wallet_id = serializers.UUIDField()
    coin_amount = serializers.DecimalField(max_digits=24, decimal_places=8, min_value=Decimal("0.00000001"))


class MiningJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiningJob
        fields = "__all__"


class MiningJobCreateSerializer(serializers.Serializer):
    machine_id = serializers.UUIDField()
    wallet_id = serializers.UUIDField()
    coin_slug = serializers.SlugField()
    miner_software_id = serializers.UUIDField(required=False)
    mode = serializers.ChoiceField(choices=["cpu", "gpu"], default="cpu")
