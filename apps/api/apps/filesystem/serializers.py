from rest_framework import serializers

from .models import FileNode, FilePermission


class FileNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileNode
        fields = [
            "id",
            "machine",
            "parent",
            "owner",
            "name",
            "path",
            "kind",
            "file_type",
            "mime_type",
            "content",
            "size_bytes",
            "is_hidden",
            "is_system",
            "metadata",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "machine", "parent", "owner", "name", "size_bytes", "created_at", "updated_at"]


class FileNodeCreateSerializer(serializers.Serializer):
    path = serializers.CharField(max_length=1024)
    kind = serializers.ChoiceField(choices=FileNode.Kind.choices)
    content = serializers.CharField(required=False, allow_blank=True)
    file_type = serializers.CharField(required=False, allow_blank=True, default="text")


class FileMoveCopySerializer(serializers.Serializer):
    path = serializers.CharField(max_length=1024)


class FilePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilePermission
        exclude = ["node"]

