from django.conf import settings
from django.db import models

from apps.common.models.base import UUIDModel


class PersistedJob(UUIDModel):
    class Kind(models.TextChoices):
        MINING = "mining", "Mining"
        CRACKING = "cracking", "Cracking"
        DELIVERY = "delivery", "Delivery"
        GENERIC = "generic", "Generic"

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        CLAIMED = "claimed", "Claimed"
        RUNNING = "running", "Running"
        RETRYING = "retrying", "Retrying"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"

    kind = models.CharField(max_length=40, choices=Kind.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    actor_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="persisted_jobs")
    machine = models.ForeignKey("machines.Machine", null=True, blank=True, on_delete=models.CASCADE, related_name="persisted_jobs")
    domain_object_type = models.CharField(max_length=80, blank=True)
    domain_object_id = models.CharField(max_length=80, blank=True)
    priority = models.IntegerField(default=100)
    run_after = models.DateTimeField()
    locked_by = models.CharField(max_length=120, blank=True)
    locked_at = models.DateTimeField(null=True, blank=True)
    heartbeat_at = models.DateTimeField(null=True, blank=True)
    attempt_count = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)
    progress_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    payload_json = models.JSONField(default=dict, blank=True)
    result_json = models.JSONField(default=dict, blank=True)
    error_code = models.CharField(max_length=80, blank=True)
    error_message = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "run_after", "priority", "locked_at"]),
            models.Index(fields=["kind", "status"]),
            models.Index(fields=["machine", "status"]),
        ]


