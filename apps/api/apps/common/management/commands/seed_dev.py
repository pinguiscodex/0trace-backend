from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed local development data."

    def handle(self, *args, **options):
        call_command("seed_core")
        self.stdout.write(self.style.SUCCESS("seed_dev completed"))

