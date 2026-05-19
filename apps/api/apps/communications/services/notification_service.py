from django.utils import timezone

from apps.communications.models import Notification


def notify(*, user, title: str, body: str = "", kind: str = "system", metadata: dict | None = None):
    return Notification.objects.create(user=user, title=title, body=body, kind=kind, metadata=metadata or {})


def mark_read(notification, user):
    notification = Notification.objects.get(id=notification.id, user=user)
    notification.read_at = notification.read_at or timezone.now()
    notification.save()
    return notification


def mark_all_read(user):
    Notification.objects.filter(user=user, read_at__isnull=True).update(read_at=timezone.now())

