from django.utils import timezone

from apps.progression.models import TutorialMissionDefinition, UserTutorialProgress


def bootstrap_tutorials(user):
    for mission in TutorialMissionDefinition.objects.filter(active=True):
        UserTutorialProgress.objects.get_or_create(user=user, mission=mission)


def complete_step(*, user, mission, step_key: str):
    progress, _ = UserTutorialProgress.objects.get_or_create(user=user, mission=mission)
    completed = set(progress.completed_steps)
    completed.add(step_key)
    progress.completed_steps = sorted(completed)
    steps = mission.steps or []
    progress.current_step = min(len(completed), len(steps))
    if steps and len(completed) >= len(steps):
        progress.completed_at = progress.completed_at or timezone.now()
    progress.save()
    return progress

