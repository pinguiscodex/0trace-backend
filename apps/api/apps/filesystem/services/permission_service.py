from apps.common.api.errors import GameAPIException
from apps.filesystem.models import FilePermission


def ensure_permission(node, user, *, write: bool = False):
    if node.owner_id == user.id:
        return
    perms, _ = FilePermission.objects.get_or_create(node=node)
    if write and not perms.public_write:
        raise GameAPIException("Permission denied.", code="permission_denied", status_code=403)
    if not write and not perms.public_read:
        raise GameAPIException("Permission denied.", code="permission_denied", status_code=403)


def update_permissions(node, *, user, values: dict):
    if node.owner_id != user.id:
        raise GameAPIException("Permission denied.", code="permission_denied", status_code=403)
    perms, _ = FilePermission.objects.get_or_create(node=node)
    for field in [
        "owner_read",
        "owner_write",
        "owner_execute",
        "public_read",
        "public_write",
        "public_execute",
        "privileged",
    ]:
        if field in values:
            setattr(perms, field, bool(values[field]))
    perms.save()
    return perms

