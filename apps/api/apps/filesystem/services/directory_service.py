from apps.filesystem.models import FileNode, FilePermission
from apps.filesystem.services.path_service import basename, normalize_path, parent_path


DEFAULT_DIRS = ["/", "/home", "/apps", "/etc", "/var", "/var/log", "/tmp", "/sites", "/software"]


def ensure_directory(machine, owner, path: str, *, system: bool = False):
    path = normalize_path(path)
    if path == "/":
        parent = None
    else:
        parent = ensure_directory(machine, owner, parent_path(path) or "/", system=system)
    node, _ = FileNode.objects.get_or_create(
        machine=machine,
        path=path,
        defaults={"parent": parent, "owner": owner, "name": basename(path), "kind": FileNode.Kind.DIRECTORY, "is_system": system},
    )
    FilePermission.objects.get_or_create(node=node)
    return node


def bootstrap_filesystem(machine):
    owner = machine.owner
    for path in DEFAULT_DIRS:
        ensure_directory(machine, owner, path, system=path not in {"/home", "/tmp"})
    ensure_directory(machine, owner, f"/home/{owner.handle}")

