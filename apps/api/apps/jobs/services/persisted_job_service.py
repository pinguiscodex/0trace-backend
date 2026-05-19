from django.utils import timezone

from apps.jobs.models import PersistedJob


def create_job(*, kind: str, actor_user=None, machine=None, domain_object=None, run_after=None, payload=None) -> PersistedJob:
    job = PersistedJob.objects.create(
        kind=kind,
        actor_user=actor_user,
        machine=machine,
        domain_object_type=domain_object.__class__.__name__ if domain_object is not None else "",
        domain_object_id=str(domain_object.id) if domain_object is not None else "",
        run_after=run_after or timezone.now(),
        payload_json=payload or {},
    )
    return job
