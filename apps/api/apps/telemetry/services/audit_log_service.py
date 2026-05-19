from __future__ import annotations

from apps.telemetry.models import AuditLog


def request_ip(request) -> str | None:
    if request is None:
        return None
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def audit(*, actor, event_type: str, request=None, metadata: dict | None = None) -> AuditLog:
    return AuditLog.objects.create(
        actor=actor if getattr(actor, "is_authenticated", True) else None,
        event_type=event_type,
        request_id=getattr(request, "request_id", "") if request is not None else "",
        ip_address=request_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "") if request is not None else "",
        metadata=metadata or {},
    )

