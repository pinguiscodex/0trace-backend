from django.db import transaction

from apps.common.api.errors import GameAPIException
from apps.filesystem.models import FileNode
from apps.filesystem.services.directory_service import ensure_directory
from apps.filesystem.services.file_service import create_node
from apps.software.models import ActiveSoftwareSelection, SoftwareFile


STARTER_SOFTWARE = [
    ("Starter Firewall.fw", "firewall", {"defense": 1}),
    ("Starter Waterwall.ww", "waterwall", {"waterwall": 1}),
    ("Starter Cracker.crk", "cracker", {"cracking": 1}),
    ("Starter Miner.min", "miner", {"mining": 1}),
]


def bootstrap_starter_software(machine):
    ensure_directory(machine, machine.owner, "/software")
    for name, software_type, stats in STARTER_SOFTWARE:
        path = f"/software/{name}"
        node = machine.file_nodes.filter(path=path).first()
        if node is None:
            node = create_node(machine=machine, user=machine.owner, path=path, kind=FileNode.Kind.FILE, content="", file_type=software_type)
        software, _ = SoftwareFile.objects.get_or_create(
            machine=machine,
            owner=machine.owner,
            software_type=software_type,
            name=name,
            defaults={"file_node": node, "base_stats": stats},
        )
        ActiveSoftwareSelection.objects.get_or_create(machine=machine, app_slug=software_type, defaults={"software_file": software})


@transaction.atomic
def select_software(*, user, machine, app_slug: str, software_file_id):
    if machine.owner_id != user.id:
        raise GameAPIException("Machine not found.", code="not_found", status_code=404)
    software = SoftwareFile.objects.get(id=software_file_id, machine=machine, owner=user)
    selection, _ = ActiveSoftwareSelection.objects.update_or_create(
        machine=machine,
        app_slug=app_slug,
        defaults={"software_file": software},
    )
    return selection

