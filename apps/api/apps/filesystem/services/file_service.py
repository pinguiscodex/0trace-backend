from django.db import transaction

from apps.common.api.errors import GameAPIException
from apps.filesystem.models import FileNode, FilePermission
from apps.filesystem.services.path_service import basename, normalize_path, parent_path
from apps.filesystem.services.permission_service import ensure_permission


@transaction.atomic
def create_node(*, machine, user, path: str, kind: str, content: str = "", file_type: str = "text"):
    path = normalize_path(path)
    parent = None
    if path != "/":
        parent = FileNode.objects.get(machine=machine, path=parent_path(path) or "/")
        ensure_permission(parent, user, write=True)
        if parent.kind != FileNode.Kind.DIRECTORY:
            raise GameAPIException("Parent is not a directory.", code="validation_error")
    node = FileNode.objects.create(
        machine=machine,
        parent=parent,
        owner=user,
        name=basename(path),
        path=path,
        kind=kind,
        content=content if kind == FileNode.Kind.FILE else "",
        size_bytes=len(content.encode("utf-8")) if kind == FileNode.Kind.FILE else 0,
        file_type=file_type if kind == FileNode.Kind.FILE else "",
    )
    FilePermission.objects.create(node=node)
    return node


@transaction.atomic
def update_file(*, node, user, content: str | None = None, metadata: dict | None = None):
    ensure_permission(node, user, write=True)
    if node.kind != FileNode.Kind.FILE:
        raise GameAPIException("Only files have editable content.", code="validation_error")
    if content is not None:
        node.content = content
        node.size_bytes = len(content.encode("utf-8"))
    if metadata is not None:
        node.metadata = metadata
    node.save()
    return node


@transaction.atomic
def move_node(*, node, user, new_path: str):
    ensure_permission(node, user, write=True)
    new_path = normalize_path(new_path)
    parent = FileNode.objects.get(machine=node.machine, path=parent_path(new_path) or "/")
    node.parent = parent
    node.name = basename(new_path)
    node.path = new_path
    node.save()
    return node


@transaction.atomic
def copy_node(*, node, user, new_path: str):
    ensure_permission(node, user)
    return create_node(machine=node.machine, user=user, path=new_path, kind=node.kind, content=node.content, file_type=node.file_type)

