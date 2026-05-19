from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.common.api.errors import GameAPIException
from apps.jobs.models import PersistedJob
from apps.jobs.services.job_completion_service import succeed_job
from apps.jobs.services.persisted_job_service import create_job
from apps.networking.models import CrackJob
from apps.networking.services.ip_service import resolve_fictional_ip
from apps.software.models import ActiveSoftwareSelection, SoftwareFile
from apps.telemetry.services.audit_log_service import audit
from apps.telemetry.services.security_event_service import security_event


def _get_active_software_level(machine, app_slug: str) -> int:
    try:
        selection = ActiveSoftwareSelection.objects.get(machine=machine, app_slug=app_slug)
        return selection.software_file.level
    except ActiveSoftwareSelection.DoesNotExist:
        return 0


def _get_os_processing_modifier(machine) -> Decimal:
    os_multiplier = Decimal("1.0")
    if hasattr(machine, "installed_os") and machine.installed_os:
        pct = machine.installed_os.os.modifiers.get("processing_speed_pct", 0)
        os_multiplier += Decimal(str(pct)) / Decimal("100")
    return os_multiplier


@transaction.atomic
def create_crack_job(*, user, attacker_machine, target_ip: str, cracker_software=None, request=None):
    if attacker_machine.owner_id != user.id:
        raise GameAPIException("Machine not found.", code="not_found", status_code=404)
    target = resolve_fictional_ip(target_ip)
    if target is None:
        crack = CrackJob.objects.create(attacker=user, attacker_machine=attacker_machine, target_ip=target_ip, status=CrackJob.Status.FAILED, failure_code="target_not_found")
        audit(actor=user, event_type="crack_job_failed", request=request, metadata={"crack_job": str(crack.id), "code": "target_not_found"})
        raise GameAPIException("Target not found.", code="target_not_found", status_code=404)
    if target.owner_id == user.id:
        raise GameAPIException("Cannot crack your own machine.", code="validation_error")

    attacker_waterwall_level = _get_active_software_level(attacker_machine, "waterwall")
    target_firewall_level = _get_active_software_level(target, "firewall")

    if attacker_waterwall_level < target_firewall_level:
        crack = CrackJob.objects.create(
            attacker=user, attacker_machine=attacker_machine, target_ip=target_ip,
            status=CrackJob.Status.FAILED, failure_code="waterwall_too_low",
            metadata={"attacker_waterwall": attacker_waterwall_level, "target_firewall": target_firewall_level}
        )
        audit(actor=user, event_type="crack_job_failed", request=request, metadata={"crack_job": str(crack.id), "code": "waterwall_too_low"})
        raise GameAPIException(
            "Your Waterwall level is too low to crack this target. Upgrade your Waterwall first.",
            code="waterwall_too_low", status_code=400
        )

    os_modifier = _get_os_processing_modifier(attacker_machine)
    base_duration = max(30, 300 - int(getattr(cracker_software, "level", 1)) * 10)
    duration = max(10, int(Decimal(str(base_duration)) / os_modifier)) if os_modifier > 0 else base_duration

    crack = CrackJob.objects.create(attacker=user, attacker_machine=attacker_machine, target_machine=target, target_ip=target_ip, cracker_software=cracker_software, duration_seconds=duration)
    job = create_job(kind=PersistedJob.Kind.CRACKING, actor_user=user, machine=attacker_machine, domain_object=crack, payload={"target_ip": target_ip})
    crack.persisted_job = job
    crack.save(update_fields=["persisted_job", "updated_at"])
    security_event(actor=user, machine=target, event_type="crack_job_start", severity="warning", message="A crack attempt started.", metadata={"crack_job": str(crack.id)})
    audit(actor=user, event_type="crack_job_start", request=request, metadata={"crack_job": str(crack.id)})
    return crack


@transaction.atomic
def complete_crack_job(crack_job: CrackJob):
    crack_job = CrackJob.objects.select_for_update().get(id=crack_job.id)
    if crack_job.status in {CrackJob.Status.SUCCEEDED, CrackJob.Status.FAILED, CrackJob.Status.CANCELLED}:
        return crack_job
    crack_job.status = CrackJob.Status.SUCCEEDED
    crack_job.completed_at = timezone.now()
    crack_job.save()
    if crack_job.persisted_job:
        succeed_job(crack_job.persisted_job, result={"status": "succeeded"})
    security_event(actor=crack_job.attacker, machine=crack_job.target_machine, event_type="crack_job_succeeded", severity="critical", message="A crack attempt succeeded.", metadata={"crack_job": str(crack_job.id)})
    return crack_job


@transaction.atomic
def cancel_crack_job(*, user, crack_job: CrackJob):
    crack_job = CrackJob.objects.select_for_update().get(id=crack_job.id, attacker=user)
    if crack_job.status in {CrackJob.Status.SUCCEEDED, CrackJob.Status.FAILED, CrackJob.Status.CANCELLED}:
        return crack_job
    crack_job.status = CrackJob.Status.CANCELLED
    crack_job.completed_at = timezone.now()
    crack_job.save()
    if crack_job.persisted_job:
        crack_job.persisted_job.status = PersistedJob.Status.CANCELLED
        crack_job.persisted_job.completed_at = timezone.now()
        crack_job.persisted_job.save()
    return crack_job

