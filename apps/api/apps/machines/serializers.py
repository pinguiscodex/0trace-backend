from rest_framework import serializers

from .models import AppDefinition, AppInstall, DesktopShortcut, DesktopWindowState, Machine, MachinePreference, OSDefinition, OSInstall


class DesktopShortcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesktopShortcut
        fields = ["id", "shortcut_type", "app_id", "file_path", "file_name", "grid_x", "grid_y", "created_at"]
        read_only_fields = ["id", "created_at"]


class DesktopWindowStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesktopWindowState
        fields = ["id", "windows", "active_window_id", "z_seed", "updated_at"]
        read_only_fields = ["id", "updated_at"]


class OSDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OSDefinition
        fields = "__all__"


class AppDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppDefinition
        fields = "__all__"


class AppInstallSerializer(serializers.ModelSerializer):
    app = AppDefinitionSerializer()

    class Meta:
        model = AppInstall
        fields = ["id", "app", "display_name", "active", "settings", "installed_at"]


class OSInstallSerializer(serializers.ModelSerializer):
    os = OSDefinitionSerializer()

    class Meta:
        model = OSInstall
        fields = ["id", "os", "window_manager", "installed_at", "active"]


class MachineSerializer(serializers.ModelSerializer):
    installed_os = OSInstallSerializer(read_only=True)

    class Meta:
        model = Machine
        fields = ["id", "name", "hostname", "fictional_ip", "active", "powered_on", "installed_os", "created_at", "updated_at"]


class MachinePreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachinePreference
        fields = ["theme", "desktop_settings"]


class AppCommandSerializer(serializers.Serializer):
    app_slug = serializers.SlugField()


class OSInstallCommandSerializer(serializers.Serializer):
    os_slug = serializers.SlugField()
    window_manager = serializers.CharField(required=False, allow_blank=True)

