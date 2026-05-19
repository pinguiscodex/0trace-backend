from apps.software.models import SkillDefinition, SkillProgress


def bootstrap_skills(user):
    for skill in SkillDefinition.objects.all():
        SkillProgress.objects.get_or_create(user=user, skill=skill)


def add_skill_xp(user, skill_slug: str, amount: int):
    skill = SkillDefinition.objects.get(slug=skill_slug)
    progress, _ = SkillProgress.objects.get_or_create(user=user, skill=skill)
    progress.xp += amount
    while progress.xp >= progress.level * 100 and progress.level < skill.max_level:
        progress.xp -= progress.level * 100
        progress.level += 1
    progress.save()
    return progress

