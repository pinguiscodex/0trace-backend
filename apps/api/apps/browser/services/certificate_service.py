from datetime import timedelta

from django.utils import timezone

from apps.browser.models import Certificate
from apps.common.api.errors import GameAPIException


def purchase_certificate(*, user, domain):
    if domain.owner_id != user.id:
        raise GameAPIException("Domain not found.", code="not_found", status_code=404)
    return Certificate.objects.create(domain=domain, owner=user, expires_at=timezone.now() + timedelta(days=90))

