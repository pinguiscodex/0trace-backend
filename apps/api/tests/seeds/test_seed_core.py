import pytest
from django.core.management import call_command

from apps.browser.models import PredefinedWebsite
from apps.machines.models import AppDefinition, OSDefinition


@pytest.mark.django_db
def test_seed_core_is_idempotent(seeded):
    counts = (OSDefinition.objects.count(), AppDefinition.objects.count(), PredefinedWebsite.objects.count())

    call_command("seed_core", verbosity=0)

    assert (OSDefinition.objects.count(), AppDefinition.objects.count(), PredefinedWebsite.objects.count()) == counts
    assert OSDefinition.objects.get(slug="doorsos").default_apps
    assert AppDefinition.objects.get(slug="app-store").is_uninstallable is False
    assert PredefinedWebsite.objects.filter(domain="searchable.com").exists()


@pytest.mark.django_db
def test_predefined_websites_seed_complete_documents(seeded):
    expected_domains = {
        "searchable.com",
        "microhard.com",
        "pear.com",
        "arctic.org",
        "techhub.com",
        "secondlife.com",
        "cryptfront.trade",
        "domania.com",
        "deliveries.com",
    }

    sites = PredefinedWebsite.objects.filter(domain__in=expected_domains)

    assert {site.domain for site in sites} == expected_domains
    assert all(site.html.strip() for site in sites)
    assert all(site.css.strip() for site in sites)
    assert all(site.js.strip() for site in sites)
    assert all("0trace:trusted-action" in site.js or site.domain == "searchable.com" for site in sites)
