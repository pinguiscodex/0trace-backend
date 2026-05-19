from django.conf import settings
from django.db import models

from apps.common.models.base import UUIDModel


class MailMessage(UUIDModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="sent_mail")
    subject = models.CharField(max_length=160)
    body = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="replies")
    system = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["sender", "created_at"])]


class MailRecipientState(UUIDModel):
    message = models.ForeignKey(MailMessage, on_delete=models.CASCADE, related_name="recipient_states")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mail_states")
    read_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["message", "user"], name="unique_mail_recipient_state")]
        indexes = [models.Index(fields=["user", "read_at", "created_at"])]


class Notification(UUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=160)
    body = models.TextField(blank=True)
    kind = models.CharField(max_length=60, default="system")
    read_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["user", "read_at", "created_at"])]

