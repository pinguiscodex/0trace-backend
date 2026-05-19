from django.conf import settings
from django.db import models

from apps.common.models.base import UUIDModel


class FileNode(UUIDModel):
    class Kind(models.TextChoices):
        DIRECTORY = "directory", "Directory"
        FILE = "file", "File"

    machine = models.ForeignKey("machines.Machine", on_delete=models.CASCADE, related_name="file_nodes")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="file_nodes")
    name = models.CharField(max_length=180)
    path = models.CharField(max_length=1024)
    kind = models.CharField(max_length=20, choices=Kind.choices)
    file_type = models.CharField(max_length=40, blank=True)
    mime_type = models.CharField(max_length=120, blank=True)
    content = models.TextField(blank=True)
    size_bytes = models.PositiveBigIntegerField(default=0)
    is_hidden = models.BooleanField(default=False)
    is_system = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["machine", "parent", "name"], name="unique_node_name_per_parent"),
            models.UniqueConstraint(fields=["machine", "path"], name="unique_node_path_per_machine"),
        ]
        indexes = [
            models.Index(fields=["machine", "path"]),
            models.Index(fields=["machine", "parent"]),
            models.Index(fields=["owner"]),
        ]
        ordering = ["path"]

    def __str__(self) -> str:
        return self.path


class FilePermission(UUIDModel):
    node = models.OneToOneField(FileNode, on_delete=models.CASCADE, related_name="permissions")
    owner_read = models.BooleanField(default=True)
    owner_write = models.BooleanField(default=True)
    owner_execute = models.BooleanField(default=True)
    public_read = models.BooleanField(default=False)
    public_write = models.BooleanField(default=False)
    public_execute = models.BooleanField(default=False)
    privileged = models.BooleanField(default=False)

