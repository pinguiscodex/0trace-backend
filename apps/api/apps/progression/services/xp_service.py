from apps.software.services.skill_service import add_skill_xp


def award_skill_xp(*, user, skill_slug: str, amount: int):
    return add_skill_xp(user, skill_slug, amount)

