import pytest
from django.core.management import call_command


@pytest.fixture
def seeded(db):
    call_command("seed_core", verbosity=0)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def csrf_client():
    from rest_framework.test import APIClient

    return APIClient(enforce_csrf_checks=True)

