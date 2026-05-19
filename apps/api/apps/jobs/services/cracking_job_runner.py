from apps.networking.services.crack_service import complete_crack_job


def run(job):
    return complete_crack_job(job.crack_job)

