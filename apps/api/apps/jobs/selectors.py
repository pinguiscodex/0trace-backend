from django.utils import timezone

from .models import PersistedJob


def jobs_for_user(user):
    return PersistedJob.objects.filter(actor_user=user)


def job_progress_for_user(user):
    now = timezone.now()

    mining_jobs = list(
        user.mining_jobs.select_related("coin", "miner_software")
        .filter(status__in=["queued", "running"])
        .values("id", "status", "coin__slug", "mode")
    )

    crack_jobs = list(
        user.crack_jobs.filter(status__in=["queued", "running"])
        .values("id", "status", "target_ip")
    )

    deliveries = list(
        user.deliveries.filter(status__in=["pending", "in_transit"])
        .values("id", "status", "eta")
    )

    pending_job_count = PersistedJob.objects.filter(
        actor_user=user
    ).exclude(status__in=["succeeded", "failed", "cancelled", "expired"]).count()

    return {
        "miningJobs": [
            {
                "id": str(j["id"]),
                "status": j["status"],
                "coin": j["coin__slug"],
                "mode": j["mode"],
            }
            for j in mining_jobs
        ],
        "crackJobs": [
            {
                "id": str(j["id"]),
                "status": j["status"],
                "targetIp": j["target_ip"],
            }
            for j in crack_jobs
        ],
        "deliveries": [
            {
                "id": str(d["id"]),
                "status": d["status"],
                "etaMinutes": max(0, int((d["eta"] - now).total_seconds() // 60)),
            }
            for d in deliveries
        ],
        "pendingJobCount": pending_job_count,
    }

