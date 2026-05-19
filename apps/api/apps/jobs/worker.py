from apps.jobs.services.job_claim_service import claim_next_job
from apps.jobs.tasks import run_persisted_job


def run_once(worker_id: str):
    job = claim_next_job(worker_id=worker_id)
    if job is None:
        return None
    return run_persisted_job.delay(str(job.id))

