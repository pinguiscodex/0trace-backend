from django.contrib import admin

from .models import AuditLog, SecurityEvent


class ReadOnlyAppendOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "created_at", "updated_at")

    def has_change_permission(self, request, obj=None):
        return False if obj else super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AuditLog)
class AuditLogAdmin(ReadOnlyAppendOnlyAdmin):
    list_display = ("event_type", "actor", "request_id", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("actor__handle", "request_id", "metadata")
    date_hierarchy = "created_at"


@admin.register(SecurityEvent)
class SecurityEventAdmin(ReadOnlyAppendOnlyAdmin):
    list_display = ("event_type", "severity", "actor", "machine", "created_at")
    list_filter = ("event_type", "severity", "created_at")
    search_fields = ("actor__handle", "machine__name", "message")
    date_hierarchy = "created_at"

