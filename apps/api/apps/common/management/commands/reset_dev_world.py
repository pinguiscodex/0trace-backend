from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Placeholder for local-only world reset. Does not delete data without explicit implementation."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("reset_dev_world is intentionally non-destructive."))

