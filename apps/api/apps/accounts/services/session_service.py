from django.utils import timezone

from apps.machines.services.machine_bootstrap_service import get_or_bootstrap_active_machine
from apps.hardware.models import HardwareItem


def _number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _map_app_install(install):
    return {
        "id": install.app.slug,
        "name": install.display_name,
        "installed": install.active,
        "protected": install.app.is_core or not install.app.is_uninstallable,
    }


def _map_software(file):
    modifier = ", ".join(f"{key}: {value}" for key, value in file.base_stats.items()) if file.base_stats else "base profile"
    return {
        "id": str(file.id),
        "name": file.name,
        "level": file.level,
        "type": file.software_type,
        "modifier": modifier,
    }


def _map_hardware_item(item, *, equipped_slots):
    catalog = item.catalog_item
    stats = {key: _number(value) for key, value in catalog.stats.items()}
    return {
        "id": str(item.id),
        "name": catalog.name,
        "slot": catalog.category if catalog.category != "ram" else "memory",
        "rarity": "starter" if catalog.sku.startswith("starter-") else "common",
        "equipped": str(item.id) in equipped_slots,
        "compatible": True,
        "stats": stats,
    }


def _map_mining_job(job):
    return {
        "id": str(job.id),
        "coin": job.coin.slug,
        "device": job.mode,
        "softwareId": str(job.miner_software_id) if job.miner_software_id else "",
        "status": "successful" if job.status == "completed" else job.status,
        "progress": 100 if job.status == "completed" else 0,
        "payoutPreview": str(job.total_payout),
    }


def _map_crack_job(job):
    return {
        "id": str(job.id),
        "targetIp": job.target_ip,
        "softwareId": str(job.cracker_software_id) if job.cracker_software_id else "",
        "status": "successful" if job.status == "succeeded" else job.status,
        "progress": 100 if job.status == "succeeded" else 0,
        "ruleSummary": job.metadata.get("rule_summary", ""),
        "failureReason": job.failure_code or None,
    }


def _map_wallet_balance(wallet, balance):
    return {
        "id": str(wallet.id),
        "coin": balance.coin.slug,
        "balance": str(balance.amount),
        "fictional": True,
    }


def _map_delivery(delivery):
    eta_minutes = max(0, int((delivery.eta - timezone.now()).total_seconds() // 60))
    return {
        "id": str(delivery.id),
        "status": delivery.status if delivery.status in {"pending", "in_transit", "delivered"} else "delivered",
        "label": delivery.catalog_item.name if delivery.catalog_item_id else "",
        "etaMinutes": eta_minutes,
    }


def _map_notification(notification):
    return {
        "id": str(notification.id),
        "title": notification.title,
        "body": notification.body,
        "severity": "info",
        "read": notification.read_at is not None,
        "createdAt": notification.created_at.isoformat(),
    }


def _map_skill(progress):
    next_level_xp = int(progress.skill.xp_curve.get("base", 100)) * max(progress.level, 1)
    return {
        "id": progress.skill.slug,
        "name": progress.skill.name,
        "level": progress.level,
        "xp": progress.xp,
        "nextLevelXp": next_level_xp,
        "bonus": progress.skill.category,
    }


def _map_achievement(achievement):
    return {
        "id": achievement.achievement.slug,
        "title": achievement.achievement.name,
        "description": achievement.achievement.description,
        "unlocked": True,
        "progress": 100,
    }


def _map_desktop_shortcut(shortcut):
    return {
        "id": str(shortcut.id),
        "shortcutType": shortcut.shortcut_type,
        "appId": shortcut.app_id,
        "filePath": shortcut.file_path,
        "fileName": shortcut.file_name,
        "gridX": shortcut.grid_x,
        "gridY": shortcut.grid_y,
    }


def _map_website(website):
    domain = website.domain.name if website.domain_id else f"{website.id}.local"
    return {
        "id": str(website.id),
        "domain": domain,
        "title": website.title,
        "description": website.trust_level,
        "trusted": website.site_type == "predefined",
        "html": website.html,
        "css": website.css,
        "js": website.js,
    }


def session_context(user):
    if not user.is_authenticated:
        return {"authenticated": False, "user": None}
    machine = get_or_bootstrap_active_machine(user)
    os_install = getattr(machine, "installed_os", None)
    unread_notifications = user.notifications.filter(read_at__isnull=True).count() if hasattr(user, "notifications") else 0
    app_installs = list(machine.app_installs.select_related("app"))
    equipped_slots = {str(e.item_id) for e in machine.equipped_hardware.select_related("item")}
    inventory_items = [record.item for record in machine.inventory_items.select_related("item__catalog_item")]
    equipped_items = [record.item for record in machine.equipped_hardware.select_related("item__catalog_item")]
    wallets = list(user.wallets.prefetch_related("balances__coin").filter(active=True))
    trash_items = list(HardwareItem.objects.filter(owner=user, status=HardwareItem.Status.TRASH).select_related("catalog_item"))

    cpu_power = 0
    gpu_power = 0
    ram_gb = 0
    storage_gb = 0
    for eq in machine.equipped_hardware.select_related("item__catalog_item"):
        stats = eq.item.catalog_item.stats
        category = eq.item.catalog_item.category
        if category == "cpu":
            cpu_power += _number(stats.get("processing_power") or stats.get("speed"))
        elif category == "gpu":
            gpu_power += _number(stats.get("compute_power") or stats.get("memory"))
        elif category == "ram":
            ram_gb += _number(stats.get("capacity") or stats.get("size"))
        elif category in ("ssd", "hdd"):
            storage_gb += _number(stats.get("capacity") or stats.get("size"))

    processing_power = cpu_power + gpu_power
    defense_rating = int(processing_power * 0.1 + ram_gb * 0.5)
    return {
        "authenticated": True,
        "user": {
            "id": str(user.id),
            "handle": user.handle,
            "email": user.email,
            "display_name": user.display_name,
            "preferred_language": user.preferred_language,
            "timezone": user.timezone,
            "onboarding_completed_at": user.onboarding_completed_at,
        },
        "active_machine": {
            "id": str(machine.id),
            "name": machine.name,
            "hostname": machine.hostname,
            "fictional_ip": machine.fictional_ip,
        },
        "installed_os": {
            "slug": os_install.os.slug,
            "name": os_install.os.name,
            "version": os_install.os.version,
            "theme_metadata": os_install.os.theme_metadata,
            "terminal_style": os_install.os.terminal_style,
        }
        if os_install
        else None,
        "installed_core_apps": [
            {
                "slug": app.app.slug,
                "display_name": app.display_name,
                "icon_key": app.app.icon_key,
            }
            for app in app_installs
            if app.app.is_core
        ],
        "unread_notification_count": unread_notifications,
        "tutorial": {
            "onboarding_completed_at": user.onboarding_completed_at,
        },
        "pending_jobs": {
            "count": machine.persisted_jobs.exclude(status__in=["succeeded", "failed", "cancelled", "expired"]).count()
            if hasattr(machine, "persisted_jobs")
            else 0
        },
        "machine": {
            "id": str(machine.id),
            "name": machine.name,
            "os": os_install.os.slug if os_install else "",
            "fictionalIp": machine.fictional_ip,
            "processingPower": processing_power,
            "defenseRating": defense_rating,
            "storageUsedGb": 0,
            "storageTotalGb": storage_gb,
        },
        "machineStats": {
            "processingPower": processing_power,
            "defenseRating": defense_rating,
            "storageUsedGb": 0,
            "storageTotalGb": storage_gb,
            "cpuPower": cpu_power,
            "gpuPower": gpu_power,
            "ramGb": ram_gb,
            "storageGb": storage_gb,
        },
        "installedApps": [_map_app_install(install) for install in app_installs],
        "softwareFiles": [_map_software(file) for file in machine.software_files.all()],
        "hardware": [_map_hardware_item(item, equipped_slots=equipped_slots) for item in [*inventory_items, *equipped_items]],
        "miningJobs": [_map_mining_job(job) for job in user.mining_jobs.select_related("coin", "miner_software").all()],
        "crackJobs": [_map_crack_job(job) for job in user.crack_jobs.all()],
        "mail": [],
        "wallets": [_map_wallet_balance(wallet, balance) for wallet in wallets for balance in wallet.balances.all()],
        "notifications": [_map_notification(notification) for notification in user.notifications.all()[:25]],
        "achievements": [_map_achievement(achievement) for achievement in user.achievements.select_related("achievement").all()],
        "skills": [_map_skill(progress) for progress in user.skill_progress.select_related("skill").all()],
        "deliveries": [_map_delivery(delivery) for delivery in user.deliveries.select_related("catalog_item").exclude(status__in=["claimed", "cancelled", "failed"])],
        "websites": [_map_website(website) for website in user.websites.select_related("domain").all()],
        "desktopShortcuts": [_map_desktop_shortcut(sc) for sc in machine.desktop_shortcuts.all()],
        "desktopWindowState": {
            "windows": machine.desktop_window_state.windows if hasattr(machine, "desktop_window_state") and machine.desktop_window_state else {},
            "activeWindowId": machine.desktop_window_state.active_window_id if hasattr(machine, "desktop_window_state") and machine.desktop_window_state else None,
            "zSeed": machine.desktop_window_state.z_seed if hasattr(machine, "desktop_window_state") and machine.desktop_window_state else 0,
        },
        "trash": [
            {
                "id": str(item.id),
                "name": item.catalog_item.name,
                "slot": item.catalog_item.category if item.catalog_item.category != "ram" else "memory",
                "rarity": "starter" if item.catalog_item.sku.startswith("starter-") else "common",
                "stats": {key: _number(value) for key, value in item.catalog_item.stats.items()},
                "serialNumber": item.serial_number,
                "deletedAt": item.updated_at.isoformat(),
            }
            for item in trash_items
        ],
    }
