from rest_framework import serializers

from .models import AuditLog, SecurityEvent


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ["id", "event_type", "request_id", "metadata", "created_at"]


class SecurityEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityEvent
        fields = ["id", "machine", "event_type", "severity", "message", "metadata", "created_at"]

