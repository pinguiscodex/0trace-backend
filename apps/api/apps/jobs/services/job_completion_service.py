from django.db import transaction
from django.utils import timezone

from apps.jobs.models import PersistedJob


@transaction.atomic
def succeed_job(job, *, result=None):
    job = PersistedJob.objects.select_for_update().get(id=job.id)
    if job.status == PersistedJob.Status.SUCCEEDED:
        return job
    job.status = PersistedJob.Status.SUCCEEDED
    job.progress_pct = 100
    job.result_json = result or {}
    job.completed_at = timezone.now()
    job.save()
    return job


@transaction.atomic
def fail_job(job, *, code: str, message: str):
    job = PersistedJob.objects.select_for_update().get(id=job.id)
    job.status = PersistedJob.Status.FAILED
    job.error_code = code
    job.error_message = message
    job.completed_at = timezone.now()
    job.save()
    return job

