from rest_framework import serializers

from .models import Delivery, DeliverySubscription, EquippedHardware, HardwareCatalogItem, HardwareItem, InventoryItem


class HardwareCatalogItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareCatalogItem
        fields = "__all__"


class HardwareItemSerializer(serializers.ModelSerializer):
    catalog_item = HardwareCatalogItemSerializer()

    class Meta:
        model = HardwareItem
        fields = "__all__"


class InventoryItemSerializer(serializers.ModelSerializer):
    item = HardwareItemSerializer()

    class Meta:
        model = InventoryItem
        fields = "__all__"


class EquippedHardwareSerializer(serializers.ModelSerializer):
    item = HardwareItemSerializer()

    class Meta:
        model = EquippedHardware
        fields = "__all__"


class EquipmentCommandSerializer(serializers.Serializer):
    hardware_item_id = serializers.UUIDField()
    slot = serializers.CharField(required=False, allow_blank=True, default="default")


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class DeliverySubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliverySubscription
        fields = "__all__"


class HardwarePurchaseSerializer(serializers.Serializer):
    target_machine_id = serializers.UUIDField(required=False, allow_null=True, help_text="Optional target machine for delivery")
