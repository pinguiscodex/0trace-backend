from drf_spectacular.utils import extend_schema
from apps.common.api.viewsets import EnvelopeReadOnlyModelViewSet

from .models import AuditLog, SecurityEvent
from .serializers import AuditLogSerializer, SecurityEventSerializer


@extend_schema(tags=["telemetry"])
class AuditLogViewSet(EnvelopeReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    queryset = AuditLog.objects.none()

    def get_queryset(self):
        if self.request.user.is_staff:
            return AuditLog.objects.all()
        return AuditLog.objects.filter(actor=self.request.user)


@extend_schema(tags=["telemetry"])
class SecurityEventViewSet(EnvelopeReadOnlyModelViewSet):
    serializer_class = SecurityEventSerializer
    queryset = SecurityEvent.objects.none()

    def get_queryset(self):
        if self.request.user.is_staff:
            return SecurityEvent.objects.all()
        return SecurityEvent.objects.filter(actor=self.request.user)
