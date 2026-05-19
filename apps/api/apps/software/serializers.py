from rest_framework import serializers

from .models import ActiveSoftwareSelection, SkillDefinition, SkillProgress, SoftwareFile


class SoftwareFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareFile
        fields = "__all__"


class ActiveSoftwareSelectionSerializer(serializers.ModelSerializer):
    software_file = SoftwareFileSerializer()

    class Meta:
        model = ActiveSoftwareSelection
        fields = ["id", "app_slug", "software_file"]


class SoftwareSelectSerializer(serializers.Serializer):
    app_slug = serializers.SlugField()
    software_file_id = serializers.UUIDField()


class SkillDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillDefinition
        fields = "__all__"


class SkillProgressSerializer(serializers.ModelSerializer):
    skill = SkillDefinitionSerializer()

    class Meta:
        model = SkillProgress
        fields = ["id", "skill", "level", "xp", "created_at", "updated_at"]

