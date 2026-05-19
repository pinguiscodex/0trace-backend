from .models import CrackJob


def crack_jobs_for_user(user):
    return CrackJob.objects.filter(attacker=user)

