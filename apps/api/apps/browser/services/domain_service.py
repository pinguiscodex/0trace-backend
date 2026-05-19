from urllib.parse import urlparse

from django.db import transaction

from apps.common.api.errors import GameAPIException
from apps.browser.models import Domain


def normalize_domain(value: str) -> str:
    value = value.strip().lower()
    if "://" in value:
        parsed = urlparse(value)
        value = parsed.netloc
    value = value.removeprefix("www.")
    if not value or "." not in value or "/" in value:
        raise GameAPIException("Invalid in-game domain.", code="validation_error")
    return value


@transaction.atomic
def purchase_domain(*, user, name: str, machine=None):
    normalized = normalize_domain(name)
    if Domain.objects.filter(name=normalized, status="active").exists():
        raise GameAPIException("Domain is unavailable.", code="domain_unavailable", status_code=409)
    return Domain.objects.create(name=normalized, owner=user, machine=machine)

