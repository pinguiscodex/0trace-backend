from django.conf import settings
from django.db import models

from apps.common.models.base import UUIDModel


class Domain(UUIDModel):
    name = models.CharField(max_length=253, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="domains")
    machine = models.ForeignKey("machines.Machine", null=True, blank=True, on_delete=models.SET_NULL, related_name="domains")
    status = models.CharField(max_length=20, default="active")
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["name"]), models.Index(fields=["owner", "status"])]


class Certificate(UUIDModel):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="certificates")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="certificates")
    status = models.CharField(max_length=20, default="active")
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["domain", "status"]), models.Index(fields=["owner", "status"])]


class Website(UUIDModel):
    class SiteType(models.TextChoices):
        PREDEFINED = "predefined", "Predefined"
        USER_HOSTED = "user_hosted", "User Hosted"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="websites")
    domain = models.OneToOneField(Domain, null=True, blank=True, on_delete=models.SET_NULL, related_name="website")
    title = models.CharField(max_length=160)
    site_type = models.CharField(max_length=30, choices=SiteType.choices, default=SiteType.USER_HOSTED)
    trust_level = models.CharField(max_length=30, default="untrusted")
    html = models.TextField(blank=True)
    css = models.TextField(blank=True)
    js = models.TextField(blank=True)
    sandbox_policy = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default="draft")
    content_version = models.PositiveIntegerField(default=1)

    class Meta:
        indexes = [models.Index(fields=["owner", "status"]), models.Index(fields=["site_type", "trust_level"])]


class WebsiteFile(UUIDModel):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="files")
    path = models.CharField(max_length=500)
    content_type = models.CharField(max_length=80, default="text/html")
    content = models.TextField(blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["website", "path"], name="unique_website_file_path")]


class WebsiteDeployment(UUIDModel):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="deployments")
    machine = models.ForeignKey("machines.Machine", on_delete=models.CASCADE, related_name="website_deployments")
    status = models.CharField(max_length=20, default="active")
    deployed_at = models.DateTimeField(auto_now_add=True)


class PredefinedWebsite(UUIDModel):
    domain = models.CharField(max_length=253, unique=True)
    title = models.CharField(max_length=160)
    behavior_key = models.CharField(max_length=80)
    html = models.TextField(blank=True)
    css = models.TextField(blank=True)
    js = models.TextField(blank=True)
    trust_level = models.CharField(max_length=30, default="trusted")
    metadata = models.JSONField(default=dict, blank=True)


class SearchIndexEntry(UUIDModel):
    domain = models.CharField(max_length=253, db_index=True)
    url = models.CharField(max_length=500)
    title = models.CharField(max_length=160)
    body = models.TextField(blank=True)
    site_type = models.CharField(max_length=30)
    trust_level = models.CharField(max_length=30)
    website = models.ForeignKey(Website, null=True, blank=True, on_delete=models.CASCADE, related_name="search_entries")
    predefined_website = models.ForeignKey(PredefinedWebsite, null=True, blank=True, on_delete=models.CASCADE, related_name="search_entries")

    class Meta:
        indexes = [models.Index(fields=["domain", "site_type", "trust_level"])]

