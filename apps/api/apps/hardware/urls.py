from django.urls import path

from .views import (
    DeliveryCancelSubscriptionView,
    DeliveryClaimView,
    DeliveryDetailView,
    DeliveryListView,
    DeliverySubscribeView,
    DeliverySubscriptionView,
    EquipView,
    EquipmentView,
    HardwareCatalogView,
    HardwareCatalogPurchaseView,
    InventoryView,
    UnequipView,
    HardwareTrashView,
    HardwareRestoreView,
    HardwareDeleteView,
    HardwareTrashListView,
)

urlpatterns = [
    path("hardware/catalog/", HardwareCatalogView.as_view(), name="hardware-catalog"),
    path("hardware/catalog/<str:sku>/purchase/", HardwareCatalogPurchaseView.as_view(), name="hardware-catalog-purchase"),
    path("machines/<uuid:machine_id>/inventory/", InventoryView.as_view(), name="machine-inventory"),
    path("machines/<uuid:machine_id>/equipment/", EquipmentView.as_view(), name="machine-equipment"),
    path("machines/<uuid:machine_id>/equipment/equip/", EquipView.as_view(), name="machine-equip"),
    path("machines/<uuid:machine_id>/equipment/unequip/", UnequipView.as_view(), name="machine-unequip"),
    path("deliveries/", DeliveryListView.as_view(), name="deliveries"),
    path("deliveries/<uuid:delivery_id>/", DeliveryDetailView.as_view(), name="delivery-detail"),
    path("deliveries/<uuid:delivery_id>/claim/", DeliveryClaimView.as_view(), name="delivery-claim"),
    path("delivery-subscription/", DeliverySubscriptionView.as_view(), name="delivery-subscription"),
    path("delivery-subscription/subscribe/", DeliverySubscribeView.as_view(), name="delivery-subscribe"),
    path("delivery-subscription/cancel/", DeliveryCancelSubscriptionView.as_view(), name="delivery-cancel"),
    path("hardware/trash/", HardwareTrashListView.as_view(), name="hardware-trash-list"),
    path("hardware/items/<uuid:hardware_item_id>/trash/", HardwareTrashView.as_view(), name="hardware-trash"),
    path("hardware/items/<uuid:hardware_item_id>/restore/", HardwareRestoreView.as_view(), name="hardware-restore"),
    path("hardware/items/<uuid:hardware_item_id>/", HardwareDeleteView.as_view(), name="hardware-delete"),
]

