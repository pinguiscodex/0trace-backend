from rest_framework.routers import DefaultRouter

from .views import AuditLogViewSet, SecurityEventViewSet

router = DefaultRouter()
router.register("audit-logs", AuditLogViewSet, basename="audit-log")
router.register("security-events", SecurityEventViewSet, basename="security-event")

urlpatterns = router.urls

