from config.celery import app
from apps.jobs.models import PersistedJob


@app.task
def run_persisted_job(job_id: str):
    job = PersistedJob.objects.get(id=job_id)
    if job.kind == PersistedJob.Kind.MINING:
        from apps.jobs.services.mining_job_runner import run
    elif job.kind == PersistedJob.Kind.CRACKING:
        from apps.jobs.services.cracking_job_runner import run
    elif job.kind == PersistedJob.Kind.DELIVERY:
        from apps.jobs.services.delivery_job_runner import run
    else:
        return None
    return run(job)

