from datetime import timedelta

from django.utils import timezone

from apps.common.api.errors import GameAPIException
from apps.networking.models import SimulatedLoginAttempt, SimulatedRemoteSession
from apps.networking.services.ip_service import resolve_fictional_ip
from apps.telemetry.services.security_event_service import security_event


def simulated_ssh_login(*, actor, source_machine, target_ip: str, token: str):
    target = resolve_fictional_ip(target_ip)
    succeeded = bool(target and token == f"token:{target.owner.handle}")
    SimulatedLoginAttempt.objects.create(actor=actor, source_machine=source_machine, target_machine=target, target_ip=target_ip, succeeded=succeeded, failure_code="" if succeeded else "permission_denied")
    if not succeeded:
        if target:
            security_event(actor=actor, machine=target, event_type="simulated_ssh_failure", severity="warning", message="Failed SSH login.", metadata={"source_machine": str(source_machine.id)})
        raise GameAPIException("Simulated SSH login failed.", code="permission_denied", status_code=403)
    session = SimulatedRemoteSession.objects.create(actor=actor, source_machine=source_machine, target_machine=target, permissions=["read_public"], expires_at=timezone.now() + timedelta(hours=1))
    security_event(actor=actor, machine=target, event_type="simulated_ssh_success", severity="info", message="SSH login succeeded.", metadata={"session": str(session.id)})
    return session
