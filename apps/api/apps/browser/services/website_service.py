from django.db import transaction

from apps.browser.models import Website, WebsiteDeployment
from apps.common.api.errors import GameAPIException


def sandbox_policy():
    return {"sandbox": True, "allow_scripts": True, "allow_same_origin": False, "external_fetch": False}


def create_website(*, user, title: str, html: str = "", css: str = "", js: str = "", domain=None):
    if domain and domain.owner_id != user.id:
        raise GameAPIException("Domain not found.", code="not_found", status_code=404)
    return Website.objects.create(owner=user, title=title, html=html, css=css, js=js, domain=domain, site_type=Website.SiteType.USER_HOSTED, trust_level="untrusted", sandbox_policy=sandbox_policy())


@transaction.atomic
def publish_website(*, user, website, machine):
    website = Website.objects.select_for_update().get(id=website.id, owner=user)
    if machine.owner_id != user.id:
        raise GameAPIException("Machine not found.", code="not_found", status_code=404)
    website.status = "published"
    website.content_version += 1
    website.save()
    return WebsiteDeployment.objects.create(website=website, machine=machine, status="active")

