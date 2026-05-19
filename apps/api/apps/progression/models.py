from django.conf import settings
from django.db import models

from apps.common.models.base import UUIDModel


class TutorialMissionDefinition(UUIDModel):
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=160)
    steps = models.JSONField(default=list)
    reward = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)


class UserTutorialProgress(UUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tutorial_progress")
    mission = models.ForeignKey(TutorialMissionDefinition, on_delete=models.CASCADE, related_name="user_progress")
    current_step = models.PositiveIntegerField(default=0)
    completed_steps = models.JSONField(default=list, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "mission"], name="unique_tutorial_progress_per_user")]


class AchievementDefinition(UUIDModel):
    slug = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    criteria = models.JSONField(default=dict)
    reward = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)


class UserAchievement(UUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.ForeignKey(AchievementDefinition, on_delete=models.CASCADE, related_name="user_achievements")
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "achievement"], name="unique_user_achievement")]

