from django.db import transaction

from apps.common.api.errors import GameAPIException
from apps.machines.models import OSDefinition, OSInstall
from apps.telemetry.services.audit_log_service import audit


@transaction.atomic
def install_os(*, user, machine, os_slug: str, window_manager: str = "", request=None):
    if machine.owner_id != user.id:
        raise GameAPIException("Machine not found.", code="not_found", status_code=404)
    os_definition = OSDefinition.objects.get(slug=os_slug)
    allowed = os_definition.allowed_window_managers
    if window_manager and allowed and window_manager not in allowed:
        raise GameAPIException("Window manager is not allowed for this OS.", code="validation_error")
    install, _ = OSInstall.objects.update_or_create(
        machine=machine,
        defaults={"os": os_definition, "installed_by": user, "window_manager": window_manager, "active": True},
    )
    audit(actor=user, event_type="os_install", request=request, metadata={"machine": str(machine.id), "os": os_slug})
    return install

