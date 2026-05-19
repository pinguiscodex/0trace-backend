from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.browser.models import PredefinedWebsite, SearchIndexEntry
from apps.common.predefined_websites import PREDEFINED_WEBSITE_CONTENT
from apps.economy.models import CoinDefinition, CoinPricePoint
from apps.hardware.models import HardwareCatalogItem
from apps.machines.models import AppDefinition, OSDefinition
from apps.progression.models import AchievementDefinition, TutorialMissionDefinition
from apps.software.models import SkillDefinition, SoftwareUpgradeRule


OS_DEFINITIONS = [
    {
        "slug": "doorsos",
        "name": "DoorsOS",
        "version": "10.0",
        "cost": Decimal("0.00"),
        "availability": "starter",
        "modifiers": {"processing_speed_pct": -20, "cracking_resistance_pct": 0, "ui_polish_bonus": 0},
        "default_apps": ["firewall", "waterwall", "cracker", "miner", "mail", "browser", "resources", "settings", "app-store", "terminal", "skills"],
        "command_set_reference": "doorsos-commands",
        "manual_references": ["doorsos-getting-started", "doorsos-terminal-guide"],
        "allowed_window_managers": [],
        "acquisition_rules": {"type": "starter", "description": "Default starter OS, included free with every new account."},
        "company_site": "microhard.com",
        "terminal_style": "windows-like",
        "theme_metadata": {"taskbar_style": "bottom", "start_menu": True, "dock": False, "window_border_radius": 0, "accent_color": "#0078D4"},
    },
    {
        "slug": "fruitos",
        "name": "FruitOS",
        "version": "14.0",
        "cost": Decimal("499.99"),
        "availability": "paid",
        "modifiers": {"processing_speed_pct": 0, "cracking_resistance_pct": -20, "ui_polish_bonus": 30},
        "default_apps": ["firewall", "waterwall", "cracker", "miner", "mail", "browser", "resources", "settings", "app-store", "terminal", "skills"],
        "command_set_reference": "fruitos-commands",
        "manual_references": ["fruitos-getting-started", "fruitos-terminal-guide"],
        "allowed_window_managers": [],
        "acquisition_rules": {"type": "paid", "price": "499.99", "description": "Premium OS with polished UI and extensive animations. Available at pear.com."},
        "company_site": "pear.com",
        "terminal_style": "macos-like",
        "theme_metadata": {"taskbar_style": "none", "start_menu": False, "dock": True, "window_border_radius": 12, "accent_color": "#A2AAAD"},
    },
    {
        "slug": "arcticos",
        "name": "ArcticOS",
        "version": "2026.01",
        "cost": Decimal("0.00"),
        "availability": "free",
        "modifiers": {"processing_speed_pct": 20, "cracking_resistance_pct": 0, "ui_polish_bonus": 10},
        "default_apps": ["firewall", "waterwall", "cracker", "miner", "mail", "browser", "resources", "settings", "app-store", "terminal", "skills"],
        "command_set_reference": "arcticos-commands",
        "manual_references": ["arcticos-getting-started", "arcticos-terminal-guide", "arcticos-window-managers"],
        "allowed_window_managers": ["fruitly", "carpened"],
        "acquisition_rules": {"type": "free", "description": "Free & Open Source OS. Choose your window manager during installation."},
        "company_site": "arctic.org",
        "terminal_style": "unix-like",
        "theme_metadata": {"taskbar_style": "top-panel", "start_menu": False, "dock": False, "window_border_radius": 4, "accent_color": "#3584E4"},
    },
]

APP_DEFINITIONS = [
    ("firewall", "Firewall", "security", True, True, "shield", ["fw"]),
    ("waterwall", "Waterwall", "security", True, True, "waves", ["ww"]),
    ("cracker", "Cracker", "tools", False, True, "key", ["crack"]),
    ("miner", "Miner", "economy", False, True, "pickaxe", ["mine"]),
    ("mail", "Mail", "communications", True, True, "mail", []),
    ("browser", "Browser", "browser", True, True, "globe", []),
    ("webserver", "Webserver", "browser", False, True, "server", ["webserver"]),
    ("resources", "Resources", "system", True, False, "activity", []),
    ("settings", "Settings", "system", True, False, "settings", []),
    ("app-store", "App Store", "system", True, False, "shopping-bag", []),
    ("terminal", "Terminal", "system", True, True, "terminal", []),
    ("skills", "Skills", "progression", True, True, "sparkles", []),
]

PREDEFINED_WEBSITES = [
    ("searchable.com", "Searchable", "search"),
    ("microhard.com", "Microhard", "doorsos_store"),
    ("pear.com", "Pear", "fruitos_store"),
    ("arctic.org", "ArcticOS Community", "arcticos_store"),
    ("techhub.com", "TechHub", "hardware_store"),
    ("secondlife.com", "SecondLife", "marketplace"),
    ("cryptfront.trade", "CryptFront Trade", "economy"),
    ("domania.com", "Domania", "domain_store"),
    ("deliveries.com", "Deliveries", "deliveries"),
]

HARDWARE = [
    ("starter-cpu", "Trace Celerity 100", "cpu", "25.00", {"cpu_power": "1.0"}),
    ("starter-motherboard", "Trace Board A1", "motherboard", "30.00", {}),
    ("starter-ram", "Trace RAM 4GB", "ram", "20.00", {"memory_gb": "4"}),
    ("starter-ssd", "Trace SSD 64GB", "ssd", "35.00", {"storage_gb": "64"}),
    ("starter-case", "Trace Case", "case", "15.00", {}),
    ("pear-p1", "Pear P1 Integrated Chip", "pear_chip", "399.00", {"cpu_power": "4", "memory_gb": "16"}),
    ("pear-p1-pro", "Pear P1 Pro Integrated Chip", "pear_chip", "599.00", {"cpu_power": "6", "memory_gb": "32"}),
    ("pear-p2", "Pear P2 Integrated Chip", "pear_chip", "899.00", {"cpu_power": "8", "memory_gb": "64"}),
    ("intel-i3", "Intel Core i3-12100", "cpu", "120.00", {"cpu_power": "2.5"}),
    ("intel-i5", "Intel Core i5-12400", "cpu", "200.00", {"cpu_power": "4.0"}),
    ("intel-i7", "Intel Core i7-12700", "cpu", "350.00", {"cpu_power": "6.5"}),
    ("intel-i9", "Intel Core i9-12900", "cpu", "550.00", {"cpu_power": "10.0"}),
    ("amd-ryzen3", "AMD Ryzen 3 5600X", "cpu", "150.00", {"cpu_power": "3.0"}),
    ("amd-ryzen5", "AMD Ryzen 5 5600X", "cpu", "220.00", {"cpu_power": "4.5"}),
    ("amd-ryzen7", "AMD Ryzen 7 5800X", "cpu", "380.00", {"cpu_power": "7.0"}),
    ("amd-ryzen9", "AMD Ryzen 9 5900X", "cpu", "600.00", {"cpu_power": "11.0"}),
    ("nvidia-gtx1650", "NVIDIA GTX 1650", "gpu", "150.00", {"gpu_power": "2.0"}),
    ("nvidia-gtx1660", "NVIDIA GTX 1660 Super", "gpu", "250.00", {"gpu_power": "3.5"}),
    ("nvidia-rtx3060", "NVIDIA RTX 3060", "gpu", "350.00", {"gpu_power": "5.0"}),
    ("nvidia-rtx3070", "NVIDIA RTX 3070", "gpu", "500.00", {"gpu_power": "7.5"}),
    ("nvidia-rtx3080", "NVIDIA RTX 3080", "gpu", "700.00", {"gpu_power": "10.0"}),
    ("nvidia-rtx3090", "NVIDIA RTX 3090", "gpu", "1200.00", {"gpu_power": "15.0"}),
    ("amd-rx6600", "AMD RX 6600", "gpu", "200.00", {"gpu_power": "3.0"}),
    ("amd-rx6700", "AMD RX 6700 XT", "gpu", "380.00", {"gpu_power": "5.5"}),
    ("amd-rx6800", "AMD RX 6800 XT", "gpu", "550.00", {"gpu_power": "8.0"}),
    ("amd-rx6900", "AMD RX 6900 XT", "gpu", "900.00", {"gpu_power": "12.0"}),
    ("ram-8gb", "Corsair Vengeance 8GB DDR4", "ram", "35.00", {"memory_gb": "8"}),
    ("ram-16gb", "Corsair Vengeance 16GB DDR4", "ram", "65.00", {"memory_gb": "16"}),
    ("ram-32gb", "Corsair Vengeance 32GB DDR4", "ram", "120.00", {"memory_gb": "32"}),
    ("ram-64gb", "Corsair Vengeance 64GB DDR4", "ram", "220.00", {"memory_gb": "64"}),
    ("hdd-500gb", "WD Blue 500GB HDD", "hdd", "40.00", {"storage_gb": "500"}),
    ("hdd-1tb", "WD Blue 1TB HDD", "hdd", "55.00", {"storage_gb": "1000"}),
    ("hdd-2tb", "WD Blue 2TB HDD", "hdd", "75.00", {"storage_gb": "2000"}),
    ("ssd-128gb", "Samsung 870 EVO 128GB SSD", "ssd", "30.00", {"storage_gb": "128"}),
    ("ssd-256gb", "Samsung 870 EVO 256GB SSD", "ssd", "45.00", {"storage_gb": "256"}),
    ("ssd-512gb", "Samsung 870 EVO 512GB SSD", "ssd", "70.00", {"storage_gb": "512"}),
    ("ssd-1tb", "Samsung 870 EVO 1TB SSD", "ssd", "110.00", {"storage_gb": "1000"}),
    ("ssd-2tb", "Samsung 870 EVO 2TB SSD", "ssd", "200.00", {"storage_gb": "2000"}),
    ("usb-32gb", "SanDisk Ultra 32GB USB", "usb", "10.00", {"storage_gb": "32"}),
    ("usb-64gb", "SanDisk Ultra 64GB USB", "usb", "15.00", {"storage_gb": "64"}),
    ("usb-128gb", "SanDisk Ultra 128GB USB", "usb", "25.00", {"storage_gb": "128"}),
    ("case-basic", "NZXT H510 Basic Case", "case", "70.00", {}),
    ("case-premium", "NZXT H710 Premium Case", "case", "150.00", {}),
    ("case-rgb", "Corsair 5000D RGB Case", "case", "180.00", {}),
    ("mobo-basic", "ASUS Prime B560M-A", "motherboard", "90.00", {}),
    ("mobo-mid", "MSI MAG B560 Tomahawk", "motherboard", "140.00", {}),
    ("mobo-premium", "ASUS ROG Strix Z690-E", "motherboard", "350.00", {}),
    ("doorsos-hdd", "WD Blue 1TB + DoorsOS", "hdd", "65.00", {"storage_gb": "1000", "includes_os": "doorsos"}),
]


class Command(BaseCommand):
    help = "Seed core 0trace game definitions idempotently."

    def handle(self, *args, **options):
        self.seed_os()
        self.seed_apps()
        self.seed_hardware()
        self.seed_coins()
        self.seed_software()
        self.seed_progression()
        self.seed_websites()
        self.stdout.write(self.style.SUCCESS("seed_core completed"))

    def seed_os(self):
        for data in OS_DEFINITIONS:
            OSDefinition.objects.update_or_create(slug=data["slug"], defaults=data)

    def seed_apps(self):
        os_names = {
            "doorsos": {},
            "fruitos": {"terminal": "Terminal", "browser": "Safari-ish"},
            "arcticos": {},
        }
        for slug, name, category, is_core, is_uninstallable, icon_key, aliases in APP_DEFINITIONS:
            AppDefinition.objects.update_or_create(
                slug=slug,
                defaults={
                    "default_display_name": name,
                    "os_display_names": {os_slug: names.get(slug, name) for os_slug, names in os_names.items()},
                    "category": category,
                    "is_core": is_core,
                    "is_uninstallable": is_uninstallable,
                    "icon_key": icon_key,
                    "terminal_command_aliases": aliases,
                },
            )

    def seed_hardware(self):
        for sku, name, category, price, stats in HARDWARE:
            HardwareCatalogItem.objects.update_or_create(
                sku=sku,
                defaults={"name": name, "category": category, "price": Decimal(price), "stats": stats},
            )

    def seed_coins(self):
        credits, _ = CoinDefinition.objects.update_or_create(slug="credits", defaults={"symbol": "CR", "name": "Credits", "is_primary": True, "difficulty": Decimal("1")})
        bittrace, _ = CoinDefinition.objects.update_or_create(slug="bittrace", defaults={"symbol": "BTR", "name": "BitTrace", "difficulty": Decimal("2.5")})
        shitcoin, _ = CoinDefinition.objects.update_or_create(slug="shitcoin", defaults={"symbol": "SHT", "name": "Shitcoin", "difficulty": Decimal("0.5")})
        now = timezone.now().replace(microsecond=0)
        for coin, price in [(credits, "1"), (bittrace, "120"), (shitcoin, "0.02")]:
            CoinPricePoint.objects.get_or_create(coin=coin, price_at=now, defaults={"price_credits": Decimal(price)})

    def seed_software(self):
        for slug, name, category in [
            ("hacking", "Hacking", "networking"),
            ("mining", "Mining", "economy"),
            ("systems", "Systems", "machine"),
            ("web", "Web", "browser"),
        ]:
            SkillDefinition.objects.update_or_create(slug=slug, defaults={"name": name, "category": category, "max_level": 100, "xp_curve": {"base": 100}})
        for software_type in ["firewall", "waterwall", "cracker", "miner", "webserver", "utility", "app_package"]:
            for level in range(2, 11):
                SoftwareUpgradeRule.objects.update_or_create(software_type=software_type, target_level=level, defaults={"required_xp": 100 * (level - 1), "modifiers": {}})

    def seed_progression(self):
        TutorialMissionDefinition.objects.update_or_create(
            slug="first-steps",
            defaults={"name": "First Steps", "steps": ["open_terminal", "open_browser", "check_mail"], "reward": {"credits": "50"}, "active": True},
        )
        AchievementDefinition.objects.update_or_create(
            slug="first-login",
            defaults={"name": "First Login", "description": "Enter your machine.", "criteria": {"event": "login_success"}, "active": True},
        )

    def seed_websites(self):
        for domain, title, behavior in PREDEFINED_WEBSITES:
            site_data = PREDEFINED_WEBSITE_CONTENT.get(domain, {})
            html = site_data.get("html", "")
            css = site_data.get("css", "")
            js = site_data.get("js", "")
            site, _ = PredefinedWebsite.objects.update_or_create(
                domain=domain,
                defaults={
                    "title": title,
                    "behavior_key": behavior,
                    "html": html,
                    "css": css,
                    "js": js,
                    "trust_level": "trusted",
                    "metadata": {"seeded": True},
                },
            )
            SearchIndexEntry.objects.update_or_create(
                domain=domain,
                url=f"https://www.{domain}",
                defaults={"title": title, "body": f"{title} {behavior}", "site_type": "predefined", "trust_level": "trusted", "predefined_website": site},
            )
