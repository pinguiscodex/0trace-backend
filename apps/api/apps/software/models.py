from django.conf import settings
from django.db import models

from apps.common.models.base import UUIDModel


class SoftwareFile(UUIDModel):
    class SoftwareType(models.TextChoices):
        FIREWALL = "firewall", "Firewall"
        WATERWALL = "waterwall", "Waterwall"
        CRACKER = "cracker", "Cracker"
        MINER = "miner", "Miner"
        WEBSERVER = "webserver", "Webserver"
        UTILITY = "utility", "Utility"
        APP_PACKAGE = "app_package", "App Package"

    machine = models.ForeignKey("machines.Machine", on_delete=models.CASCADE, related_name="software_files")
    file_node = models.OneToOneField("filesystem.FileNode", null=True, blank=True, on_delete=models.SET_NULL, related_name="software_file")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="software_files")
    name = models.CharField(max_length=120)
    software_type = models.CharField(max_length=40, choices=SoftwareType.choices)
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    base_stats = models.JSONField(default=dict, blank=True)
    transferable = models.BooleanField(default=True)
    locked_by_job = models.ForeignKey("jobs.PersistedJob", null=True, blank=True, on_delete=models.SET_NULL, related_name="locked_software")

    class Meta:
        indexes = [
            models.Index(fields=["machine", "software_type"]),
            models.Index(fields=["owner", "software_type"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} L{self.level}"


class ActiveSoftwareSelection(UUIDModel):
    machine = models.ForeignKey("machines.Machine", on_delete=models.CASCADE, related_name="active_software")
    app_slug = models.SlugField(max_length=60)
    software_file = models.ForeignKey(SoftwareFile, on_delete=models.PROTECT, related_name="active_selections")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["machine", "app_slug"], name="unique_active_software_per_app")]


class SoftwareUpgradeRule(UUIDModel):
    software_type = models.CharField(max_length=40, choices=SoftwareFile.SoftwareType.choices)
    target_level = models.PositiveIntegerField()
    required_xp = models.PositiveIntegerField()
    modifiers = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["software_type", "target_level"], name="unique_upgrade_rule")]


class SkillDefinition(UUIDModel):
    slug = models.SlugField(max_length=60, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=60)
    max_level = models.PositiveIntegerField(default=100)
    xp_curve = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return self.name


class SkillProgress(UUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="skill_progress")
    skill = models.ForeignKey(SkillDefinition, on_delete=models.CASCADE, related_name="progress")
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "skill"], name="unique_skill_progress_per_user")]


class XPEvent(UUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="xp_events")
    machine = models.ForeignKey("machines.Machine", null=True, blank=True, on_delete=models.CASCADE, related_name="xp_events")
    software_file = models.ForeignKey(SoftwareFile, null=True, blank=True, on_delete=models.CASCADE, related_name="xp_events")
    skill = models.ForeignKey(SkillDefinition, null=True, blank=True, on_delete=models.CASCADE, related_name="xp_events")
    amount = models.PositiveIntegerField()
    source = models.CharField(max_length=80)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["user", "created_at"]), models.Index(fields=["source", "created_at"])]

