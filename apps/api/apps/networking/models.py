from django.conf import settings
from django.db import models

from apps.common.models.base import UUIDModel


class CrackJob(UUIDModel):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"

    attacker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="crack_jobs")
    attacker_machine = models.ForeignKey("machines.Machine", on_delete=models.CASCADE, related_name="outgoing_crack_jobs")
    target_machine = models.ForeignKey("machines.Machine", null=True, blank=True, on_delete=models.SET_NULL, related_name="incoming_crack_jobs")
    target_ip = models.CharField(max_length=45)
    cracker_software = models.ForeignKey("software.SoftwareFile", null=True, blank=True, on_delete=models.PROTECT, related_name="crack_jobs")
    persisted_job = models.OneToOneField("jobs.PersistedJob", null=True, blank=True, on_delete=models.SET_NULL, related_name="crack_job")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    failure_code = models.CharField(max_length=80, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["attacker", "status"]),
            models.Index(fields=["target_machine", "status"]),
            models.Index(fields=["target_ip", "status"]),
        ]


class SimulatedRemoteSession(UUIDModel):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="remote_sessions")
    source_machine = models.ForeignKey("machines.Machine", on_delete=models.CASCADE, related_name="remote_sessions_started")
    target_machine = models.ForeignKey("machines.Machine", on_delete=models.CASCADE, related_name="remote_sessions_received")
    status = models.CharField(max_length=20, default="active")
    permissions = models.JSONField(default=list, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)


class SimulatedLoginAttempt(UUIDModel):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="simulated_login_attempts")
    source_machine = models.ForeignKey("machines.Machine", null=True, blank=True, on_delete=models.SET_NULL, related_name="simulated_login_attempts")
    target_machine = models.ForeignKey("machines.Machine", null=True, blank=True, on_delete=models.SET_NULL, related_name="simulated_login_attempts_received")
    target_ip = models.CharField(max_length=45)
    succeeded = models.BooleanField(default=False)
    failure_code = models.CharField(max_length=80, blank=True)

    class Meta:
        indexes = [models.Index(fields=["target_machine", "created_at"]), models.Index(fields=["actor", "created_at"])]

