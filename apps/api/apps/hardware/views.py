from datetime import timedelta

from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework.views import APIView

from apps.common.api.responses import ok
from apps.machines.models import Machine

from .models import Delivery, DeliverySubscription, HardwareCatalogItem, HardwareItem
from .serializers import (
    DeliverySerializer,
    DeliverySubscriptionSerializer,
    EquippedHardwareSerializer,
    EquipmentCommandSerializer,
    HardwareCatalogItemSerializer,
    HardwarePurchaseSerializer,
    InventoryItemSerializer,
)
from .services.delivery_service import claim_delivery
from .services.equipment_service import equip_item, unequip_item
from .services.purchase_service import purchase_hardware
from .services.trash_service import move_to_trash, restore_from_trash, delete_permanently


@extend_schema(tags=["hardware"])
class HardwareCatalogView(APIView):
    permission_classes = [AllowAny]
    serializer_class = HardwareCatalogItemSerializer

    def get(self, request):
        return ok(HardwareCatalogItemSerializer(HardwareCatalogItem.objects.all(), many=True).data)


@extend_schema(tags=["hardware"])
class HardwareCatalogPurchaseView(APIView):
    serializer_class = HardwarePurchaseSerializer

    @extend_schema(request=HardwarePurchaseSerializer, responses={201: DeliverySerializer})
    def post(self, request, sku):
        serializer = HardwarePurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the catalog item
        catalog_item = HardwareCatalogItem.objects.get(sku=sku)

        # Resolve target machine
        machine = None
        if serializer.validated_data.get("target_machine_id"):
            machine = Machine.objects.get(
                id=serializer.validated_data["target_machine_id"],
                owner=request.user
            )

        # Purchase the hardware
        delivery = purchase_hardware(
            user=request.user,
            catalog_item=catalog_item,
            machine=machine,
            request=request,
        )

        return ok(DeliverySerializer(delivery).data)


@extend_schema(tags=["hardware"])
class InventoryView(APIView):
    serializer_class = InventoryItemSerializer

    def get(self, request, machine_id):
        machine = Machine.objects.get(id=machine_id, owner=request.user)
        return ok(InventoryItemSerializer(machine.inventory_items.select_related("item__catalog_item"), many=True).data)


@extend_schema(tags=["hardware"])
class EquipmentView(APIView):
    serializer_class = EquippedHardwareSerializer

    def get(self, request, machine_id):
        machine = Machine.objects.get(id=machine_id, owner=request.user)
        return ok(EquippedHardwareSerializer(machine.equipped_hardware.select_related("item__catalog_item"), many=True).data)


@extend_schema(tags=["hardware"])
class EquipView(APIView):
    serializer_class = EquipmentCommandSerializer

    @extend_schema(request=EquipmentCommandSerializer, responses={200: dict})
    def post(self, request, machine_id):
        machine = Machine.objects.get(id=machine_id, owner=request.user)
        serializer = EquipmentCommandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = equip_item(user=request.user, machine=machine, request=request, **serializer.validated_data)
        return ok({"hardware_item_id": str(item.id), "status": item.status})


@extend_schema(tags=["hardware"])
class UnequipView(APIView):
    serializer_class = EquipmentCommandSerializer

    @extend_schema(request=EquipmentCommandSerializer, responses={200: dict})
    def post(self, request, machine_id):
        machine = Machine.objects.get(id=machine_id, owner=request.user)
        serializer = EquipmentCommandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = unequip_item(user=request.user, machine=machine, hardware_item_id=serializer.validated_data["hardware_item_id"], request=request)
        return ok({"hardware_item_id": str(item.id), "status": item.status})


@extend_schema(tags=["hardware"])
class DeliveryListView(APIView):
    serializer_class = DeliverySerializer

    @extend_schema(operation_id="deliveries_list", responses={200: DeliverySerializer(many=True)})
    def get(self, request):
        return ok(DeliverySerializer(Delivery.objects.filter(owner=request.user), many=True).data)


@extend_schema(tags=["hardware"])
class DeliveryDetailView(APIView):
    serializer_class = DeliverySerializer

    @extend_schema(operation_id="deliveries_retrieve", responses={200: DeliverySerializer})
    def get(self, request, delivery_id):
        return ok(DeliverySerializer(Delivery.objects.get(id=delivery_id, owner=request.user)).data)


@extend_schema(tags=["hardware"])
class DeliveryClaimView(APIView):
    serializer_class = DeliverySerializer

    def post(self, request, delivery_id):
        delivery = Delivery.objects.get(id=delivery_id, owner=request.user)
        return ok(DeliverySerializer(claim_delivery(user=request.user, delivery=delivery, request=request)).data)


@extend_schema(tags=["hardware"])
class DeliverySubscriptionView(APIView):
    serializer_class = DeliverySubscriptionSerializer

    def get(self, request):
        subscription, _ = DeliverySubscription.objects.get_or_create(user=request.user)
        return ok(DeliverySubscriptionSerializer(subscription).data)


@extend_schema(tags=["hardware"])
class DeliverySubscribeView(APIView):
    serializer_class = DeliverySubscriptionSerializer

    def post(self, request):
        subscription, _ = DeliverySubscription.objects.get_or_create(user=request.user)
        subscription.active = True
        subscription.expires_at = timezone.now() + timedelta(days=30)
        subscription.save()
        return ok(DeliverySubscriptionSerializer(subscription).data)


@extend_schema(tags=["hardware"])
class DeliveryCancelSubscriptionView(APIView):
    serializer_class = DeliverySubscriptionSerializer

    def post(self, request):
        subscription, _ = DeliverySubscription.objects.get_or_create(user=request.user)
        subscription.active = False
        subscription.save()
        return ok(DeliverySubscriptionSerializer(subscription).data)


@extend_schema(tags=["hardware"])
class HardwareTrashView(APIView):
    serializer_class = serializers.Serializer

    def post(self, request, hardware_item_id):
        item = move_to_trash(user=request.user, hardware_item_id=hardware_item_id, request=request)
        return ok({"hardware_item_id": str(item.id), "status": item.status})


@extend_schema(tags=["hardware"])
class HardwareRestoreView(APIView):
    serializer_class = serializers.Serializer

    def post(self, request, hardware_item_id):
        item = restore_from_trash(user=request.user, hardware_item_id=hardware_item_id, request=request)
        return ok({"hardware_item_id": str(item.id), "status": item.status})


@extend_schema(tags=["hardware"])
class HardwareDeleteView(APIView):
    serializer_class = serializers.Serializer

    def delete(self, request, hardware_item_id):
        item_id = delete_permanently(user=request.user, hardware_item_id=hardware_item_id, request=request)
        return ok({"hardware_item_id": item_id, "deleted": True})


@extend_schema(tags=["hardware"])
class HardwareTrashListView(APIView):
    serializer_class = serializers.Serializer

    def get(self, request):
        trash_items = HardwareItem.objects.filter(owner=request.user, status=HardwareItem.Status.TRASH).select_related("catalog_item")
        data = []
        for item in trash_items:
            catalog = item.catalog_item
            data.append({
                "id": str(item.id),
                "name": catalog.name,
                "slot": catalog.category if catalog.category != "ram" else "memory",
                "rarity": "starter" if catalog.sku.startswith("starter-") else "common",
                "stats": {key: float(value) for key, value in catalog.stats.items()},
                "serialNumber": item.serial_number,
                "deletedAt": item.updated_at.isoformat(),
            })
        return ok(data)
