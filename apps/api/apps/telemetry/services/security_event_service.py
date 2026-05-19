from apps.telemetry.models import SecurityEvent


def security_event(*, actor=None, machine=None, event_type: str, message: str, severity: str = "info", metadata: dict | None = None):
    return SecurityEvent.objects.create(
        actor=actor if getattr(actor, "is_authenticated", True) else None,
        machine=machine,
        event_type=event_type,
        message=message,
        severity=severity,
        metadata=metadata or {},
    )

