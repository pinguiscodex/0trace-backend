from __future__ import annotations

from django.db import transaction

from apps.common.services.ids import short_code
from apps.machines.models import AppDefinition, AppInstall, Machine, MachinePreference, OSDefinition, OSInstall


def starter_ip_for_user(user) -> str:
    value = int(user.id.hex[:6], 16)
    return f"10.{(value >> 16) & 255}.{(value >> 8) & 255}.{value & 255}"


def get_or_bootstrap_active_machine(user) -> Machine:
    machine = Machine.objects.filter(owner=user, active=True).first()
    if machine:
        return machine
    with transaction.atomic():
        return bootstrap_machine_for_user(user)


def bootstrap_machine_for_user(user) -> Machine:
    doors = OSDefinition.objects.get(slug="doorsos")
    machine, _ = Machine.objects.get_or_create(
        owner=user,
        hostname=f"{user.handle}-pc",
        defaults={
            "name": f"{user.display_name or user.handle}'s machine",
            "fictional_ip": starter_ip_for_user(user),
        },
    )
    os_install, _ = OSInstall.objects.get_or_create(machine=machine, defaults={"os": doors, "installed_by": user})
    prefs, _ = MachinePreference.objects.get_or_create(machine=machine, defaults={"active_os_install": os_install})
    if prefs.active_os_install_id is None:
        prefs.active_os_install = os_install
        prefs.save(update_fields=["active_os_install", "updated_at"])
    for app_slug in doors.default_apps:
        app = AppDefinition.objects.get(slug=app_slug)
        AppInstall.objects.get_or_create(
            machine=machine,
            app=app,
            defaults={"display_name": app.os_display_names.get(doors.slug, app.default_display_name), "installed_by": user},
        )
    try:
        from apps.filesystem.services.directory_service import bootstrap_filesystem
        from apps.software.services.software_selection_service import bootstrap_starter_software
        from apps.hardware.services.inventory_service import bootstrap_starter_hardware
        from apps.economy.services.wallet_service import bootstrap_starter_wallet
        from apps.progression.services.tutorial_service import bootstrap_tutorials
        from apps.communications.services.mail_service import send_system_mail
        from apps.communications.services.notification_service import notify

        bootstrap_filesystem(machine)
        bootstrap_starter_software(machine)
        bootstrap_starter_hardware(machine)
        bootstrap_starter_wallet(user)
        bootstrap_tutorials(user)
        send_system_mail(user=user, subject="Welcome to 0trace", body="Your machine is ready.")
        notify(user=user, title="Machine ready", body="DoorsOS and starter tools have been installed.")
    except Exception:
        raise
    return machine

