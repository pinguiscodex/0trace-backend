from rest_framework.routers import DefaultRouter

from .views import AppDefinitionViewSet, DesktopShortcutViewSet, MachineViewSet, OSDefinitionViewSet

router = DefaultRouter()
router.register("machines", MachineViewSet, basename="machine")
router.register("os", OSDefinitionViewSet, basename="os")
router.register("apps", AppDefinitionViewSet, basename="app")
router.register("desktop-shortcuts", DesktopShortcutViewSet, basename="desktop-shortcut")

urlpatterns = router.urls

