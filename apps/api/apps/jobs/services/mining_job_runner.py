from apps.economy.services.mining_service import settle_mining_job


def run(job):
    return settle_mining_job(job.mining_job)

