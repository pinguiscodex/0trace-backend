from django.db import transaction
from django.utils import timezone

from apps.jobs.models import PersistedJob


@transaction.atomic
def claim_next_job(*, worker_id: str):
    job = (
        PersistedJob.objects.select_for_update(skip_locked=True)
        .filter(status=PersistedJob.Status.QUEUED, run_after__lte=timezone.now())
        .order_by("priority", "run_after")
        .first()
    )
    if job is None:
        return None
    job.status = PersistedJob.Status.CLAIMED
    job.locked_by = worker_id
    job.locked_at = timezone.now()
    job.heartbeat_at = timezone.now()
    job.attempt_count += 1
    job.save()
    return job

