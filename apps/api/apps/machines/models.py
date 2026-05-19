from django.conf import settings
from django.db import models

from apps.common.models.base import UUIDModel


class OSDefinition(UUIDModel):
    class Availability(models.TextChoices):
        FREE = "free", "Free"
        PAID = "paid", "Paid"
        STARTER = "starter", "Starter"

    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=40, unique=True)
    version = models.CharField(max_length=40)
    cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    availability = models.CharField(max_length=20, choices=Availability.choices)
    modifiers = models.JSONField(default=dict, blank=True)
    default_apps = models.JSONField(default=list, blank=True)
    command_set_reference = models.CharField(max_length=80, blank=True)
    manual_references = models.JSONField(default=list, blank=True)
    allowed_window_managers = models.JSONField(default=list, blank=True)
    acquisition_rules = models.JSONField(default=dict, blank=True)
    company_site = models.CharField(max_length=120)
    terminal_style = models.CharField(max_length=40)
    theme_metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class AppDefinition(UUIDModel):
    slug = models.SlugField(max_length=60, unique=True)
    default_display_name = models.CharField(max_length=80)
    os_display_names = models.JSONField(default=dict, blank=True)
    category = models.CharField(max_length=40)
    is_core = models.BooleanField(default=False)
    is_uninstallable = models.BooleanField(default=True)
    icon_key = models.CharField(max_length=80)
    terminal_command_aliases = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["category", "default_display_name"]

    def __str__(self) -> str:
        return self.default_display_name


class Machine(UUIDModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="machines")
    name = models.CharField(max_length=80)
    hostname = models.SlugField(max_length=64)
    fictional_ip = models.CharField(max_length=45, unique=True)
    active = models.BooleanField(default=True)
    powered_on = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "hostname"], name="unique_machine_hostname_per_owner"),
        ]
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["fictional_ip"]),
        ]
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.name


class MachinePreference(UUIDModel):
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE, related_name="preferences")
    active_os_install = models.ForeignKey("OSInstall", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    theme = models.CharField(max_length=60, default="default")
    desktop_settings = models.JSONField(default=dict, blank=True)


class OSInstall(UUIDModel):
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE, related_name="installed_os")
    os = models.ForeignKey(OSDefinition, on_delete=models.PROTECT, related_name="installs")
    installed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="os_installs")
    window_manager = models.CharField(max_length=80, blank=True)
    installed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["machine", "active"])]


class AppInstall(UUIDModel):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="app_installs")
    app = models.ForeignKey(AppDefinition, on_delete=models.PROTECT, related_name="installs")
    display_name = models.CharField(max_length=80)
    installed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="app_installs")
    installed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["machine", "app"], name="unique_app_install_per_machine"),
        ]
        indexes = [models.Index(fields=["machine", "active"])]


class DesktopShortcut(UUIDModel):
    class ShortcutType(models.TextChoices):
        APP = "app", "App"
        FILE = "file", "File"

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="desktop_shortcuts")
    shortcut_type = models.CharField(max_length=10, choices=ShortcutType.choices)
    app_id = models.SlugField(max_length=60, null=True, blank=True)
    file_path = models.CharField(max_length=500, null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    grid_x = models.IntegerField(default=0)
    grid_y = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["machine", "app_id"],
                name="unique_app_shortcut_per_machine",
                condition=models.Q(app_id__isnull=False),
            ),
            models.UniqueConstraint(
                fields=["machine", "file_path"],
                name="unique_file_shortcut_per_machine",
                condition=models.Q(file_path__isnull=False),
            ),
        ]
        indexes = [
            models.Index(fields=["machine"]),
        ]
        ordering = ["grid_y", "grid_x", "created_at"]

    def __str__(self) -> str:
        label = self.app_id or self.file_name or self.file_path or "unknown"
        return f"{self.shortcut_type}: {label} ({self.grid_x}, {self.grid_y})"


class DesktopWindowState(UUIDModel):
    machine = models.OneToOneField(Machine, on_delete=models.CASCADE, related_name="desktop_window_state")
    windows = models.JSONField(default=dict, blank=True)
    active_window_id = models.CharField(max_length=255, null=True, blank=True)
    z_seed = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"DesktopWindowState for {self.machine.name}"



