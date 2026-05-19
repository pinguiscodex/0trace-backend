from apps.progression.models import AchievementDefinition, UserAchievement


def grant_achievement(*, user, slug: str):
    achievement = AchievementDefinition.objects.get(slug=slug)
    unlocked, _ = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
    return unlocked

