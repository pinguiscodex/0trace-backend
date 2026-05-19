from django.db import transaction

from apps.common.api.errors import GameAPIException
from apps.software.models import SoftwareFile, SoftwareUpgradeRule, XPEvent


@transaction.atomic
def add_software_xp(*, user, software_file: SoftwareFile, amount: int, source: str):
    if software_file.owner_id != user.id:
        raise GameAPIException("Software not found.", code="not_found", status_code=404)
    software_file.xp += amount
    while True:
        rule = SoftwareUpgradeRule.objects.filter(software_type=software_file.software_type, target_level=software_file.level + 1).first()
        if rule is None or software_file.xp < rule.required_xp:
            break
        software_file.xp -= rule.required_xp
        software_file.level += 1
    software_file.save()
    XPEvent.objects.create(user=user, machine=software_file.machine, software_file=software_file, amount=amount, source=source)
    return software_file


def level_up_software(*, user, software_file: SoftwareFile):
    return add_software_xp(user=user, software_file=software_file, amount=100, source="manual_level_up")

