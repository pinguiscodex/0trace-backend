from django.db import transaction

from apps.common.api.errors import GameAPIException
from apps.machines.models import AppDefinition, AppInstall
from apps.telemetry.services.audit_log_service import audit


@transaction.atomic
def install_app(*, user, machine, app_slug: str, request=None):
    if machine.owner_id != user.id:
        raise GameAPIException("Machine not found.", code="not_found", status_code=404)
    app = AppDefinition.objects.get(slug=app_slug)
    install, _ = AppInstall.objects.get_or_create(
        machine=machine,
        app=app,
        defaults={"display_name": app.default_display_name, "installed_by": user},
    )
    if not install.active:
        install.active = True
        install.save(update_fields=["active", "updated_at"])
    audit(actor=user, event_type="app_install", request=request, metadata={"machine": str(machine.id), "app": app_slug})
    return install


@transaction.atomic
def uninstall_app(*, user, machine, app_slug: str, request=None):
    if machine.owner_id != user.id:
        raise GameAPIException("Machine not found.", code="not_found", status_code=404)
    app = AppDefinition.objects.get(slug=app_slug)
    if not app.is_uninstallable:
        raise GameAPIException("This app cannot be uninstalled.", code="permission_denied", status_code=403)
    install = AppInstall.objects.select_for_update().get(machine=machine, app=app)
    install.active = False
    install.save(update_fields=["active", "updated_at"])
    audit(actor=user, event_type="app_uninstall", request=request, metadata={"machine": str(machine.id), "app": app_slug})
    return install

