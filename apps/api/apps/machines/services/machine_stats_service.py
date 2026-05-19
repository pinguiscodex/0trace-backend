from decimal import Decimal


def calculate_machine_stats(machine):
    hardware_stats = {
        "cpu_power": Decimal("1.0"),
        "gpu_power": Decimal("0.0"),
        "memory_gb": Decimal("4.0"),
        "storage_gb": Decimal("64.0"),
    }
    for equipped in machine.equipped_hardware.select_related("item__catalog_item").all() if hasattr(machine, "equipped_hardware") else []:
        stats = equipped.item.catalog_item.stats
        hardware_stats["cpu_power"] += Decimal(str(stats.get("cpu_power", "0")))
        hardware_stats["gpu_power"] += Decimal(str(stats.get("gpu_power", "0")))
        hardware_stats["memory_gb"] += Decimal(str(stats.get("memory_gb", "0")))
        hardware_stats["storage_gb"] += Decimal(str(stats.get("storage_gb", "0")))

    os_multiplier = Decimal("1.0")
    if hasattr(machine, "installed_os"):
        os_multiplier += Decimal(str(machine.installed_os.os.modifiers.get("processing_speed_pct", 0))) / Decimal("100")

    processing_power = (hardware_stats["cpu_power"] + hardware_stats["gpu_power"] * Decimal("0.75")) * os_multiplier
    return {
        "processing_power": processing_power,
        "cpu_power": hardware_stats["cpu_power"],
        "gpu_power": hardware_stats["gpu_power"],
        "memory_gb": hardware_stats["memory_gb"],
        "storage_gb": hardware_stats["storage_gb"],
        "mining_efficiency": processing_power,
        "cracking_efficiency": processing_power,
    }

