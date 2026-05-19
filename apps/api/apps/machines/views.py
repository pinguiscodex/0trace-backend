from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.common.api.viewsets import EnvelopeReadOnlyModelViewSet

from apps.common.api.responses import ok

from .models import AppDefinition, DesktopShortcut, DesktopWindowState, Machine, OSDefinition
from .serializers import (
    AppCommandSerializer,
    AppDefinitionSerializer,
    AppInstallSerializer,
    DesktopShortcutSerializer,
    DesktopWindowStateSerializer,
    MachinePreferenceSerializer,
    MachineSerializer,
    OSDefinitionSerializer,
    OSInstallCommandSerializer,
)
from .services.app_install_service import install_app, uninstall_app
from .services.machine_stats_service import calculate_machine_stats
from .services.os_install_service import install_os


@extend_schema(tags=["machines"])
class MachineViewSet(EnvelopeReadOnlyModelViewSet):
    serializer_class = MachineSerializer
    queryset = Machine.objects.none()

    def get_queryset(self):
        return Machine.objects.filter(owner=self.request.user).select_related("installed_os__os")

    @extend_schema(tags=["machines"], responses={200: dict})
    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        return ok(calculate_machine_stats(self.get_object()))

    @extend_schema(tags=["machines"], request=MachinePreferenceSerializer, responses={200: dict})
    @action(detail=True, methods=["get", "patch"], url_path="settings")
    def machine_settings(self, request, pk=None):
        machine = self.get_object()
        prefs = machine.preferences
        if request.method == "PATCH":
            serializer = MachinePreferenceSerializer(prefs, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return ok(MachinePreferenceSerializer(prefs).data)

    @extend_schema(tags=["machines"], responses={200: dict})
    @action(detail=True, methods=["post"])
    def shutdown(self, request, pk=None):
        machine = self.get_object()
        machine.powered_on = False
        machine.save(update_fields=["powered_on", "updated_at"])
        return ok({"powered_on": False})

    @extend_schema(tags=["machines"], responses={200: dict})
    @action(detail=True, methods=["post"])
    def restart(self, request, pk=None):
        machine = self.get_object()
        machine.powered_on = True
        machine.save(update_fields=["powered_on", "updated_at"])
        return ok({"powered_on": True})

    @extend_schema(tags=["machines"], responses={200: dict})
    @action(detail=True, methods=["post"])
    def logout(self, request, pk=None):
        return ok({"remote_session_closed": True})

    @extend_schema(tags=["apps"], responses={200: AppInstallSerializer(many=True)})
    @action(detail=True, methods=["get"], url_path="apps")
    def apps(self, request, pk=None):
        installs = self.get_object().app_installs.select_related("app")
        return ok(AppInstallSerializer(installs, many=True).data)

    @extend_schema(tags=["apps"], request=AppCommandSerializer, responses={200: AppInstallSerializer})
    @action(detail=True, methods=["post"], url_path="apps/install")
    def install_app(self, request, pk=None):
        serializer = AppCommandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        install = install_app(user=request.user, machine=self.get_object(), app_slug=serializer.validated_data["app_slug"], request=request)
        return ok(AppInstallSerializer(install).data)

    @extend_schema(tags=["apps"], request=AppCommandSerializer, responses={200: AppInstallSerializer})
    @action(detail=True, methods=["post"], url_path="apps/uninstall")
    def uninstall_app(self, request, pk=None):
        serializer = AppCommandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        install = uninstall_app(user=request.user, machine=self.get_object(), app_slug=serializer.validated_data["app_slug"], request=request)
        return ok(AppInstallSerializer(install).data)

    @extend_schema(tags=["os"], request=OSInstallCommandSerializer, responses={200: dict})
    @action(detail=True, methods=["post"], url_path="os/install")
    def install_os(self, request, pk=None):
        serializer = OSInstallCommandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        install = install_os(user=request.user, machine=self.get_object(), request=request, **serializer.validated_data)
        return ok({"id": str(install.id), "os": install.os.slug})

    @extend_schema(tags=["machines"], responses={200: DesktopWindowStateSerializer})
    @action(detail=True, methods=["get", "put"], url_path="desktop-state")
    def desktop_state(self, request, pk=None):
        machine = self.get_object()
        state, _ = DesktopWindowState.objects.get_or_create(machine=machine)
        if request.method == "PUT":
            serializer = DesktopWindowStateSerializer(state, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            state.refresh_from_db()
        return ok(DesktopWindowStateSerializer(state).data)


@extend_schema(tags=["os"])
class OSDefinitionViewSet(EnvelopeReadOnlyModelViewSet):
    lookup_field = "slug"
    queryset = OSDefinition.objects.all()
    serializer_class = OSDefinitionSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=["apps"])
class AppDefinitionViewSet(EnvelopeReadOnlyModelViewSet):
    queryset = AppDefinition.objects.all()
    serializer_class = AppDefinitionSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["desktop-shortcuts"])
class DesktopShortcutViewSet(EnvelopeReadOnlyModelViewSet):
    serializer_class = DesktopShortcutSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        machine = Machine.objects.filter(owner=self.request.user, active=True).first()
        if not machine:
            return DesktopShortcut.objects.none()
        return DesktopShortcut.objects.filter(machine=machine)

    def perform_create(self, serializer):
        machine = Machine.objects.filter(owner=self.request.user, active=True).first()
        if not machine:
            raise serializers.ValidationError({"machine": "No active machine found."})
        serializer.save(machine=machine)
