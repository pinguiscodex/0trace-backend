import pytest

from apps.accounts.models import User
from apps.machines.models import Machine


@pytest.mark.django_db
def test_signup_bootstraps_machine_session_and_starter_state(seeded, api_client):
    response = api_client.post(
        "/api/v1/auth/signup/",
        {
            "handle": "tracepilot",
            "email": "tracepilot@example.com",
            "password": "correct horse battery",
            "terms_accepted": True,
        },
        format="json",
    )

    assert response.status_code == 201
    payload = response.json()["data"]
    assert payload["authenticated"] is True
    assert payload["installed_os"]["slug"] == "doorsos"
    assert payload["active_machine"]["fictional_ip"].startswith("10.")
    assert {app["slug"] for app in payload["installed_core_apps"]} >= {"app-store", "settings", "resources", "terminal"}
    user = User.objects.get(handle="tracepilot")
    machine = Machine.objects.get(owner=user)
    assert machine.file_nodes.filter(path="/home/tracepilot").exists()
    assert machine.software_files.filter(software_type="firewall").exists()
    assert user.wallets.filter(balances__coin__slug="credits").exists()


@pytest.mark.django_db
def test_authenticated_unsafe_request_requires_csrf_header(seeded, csrf_client):
    csrf_response = csrf_client.get("/api/v1/auth/csrf/")
    token = csrf_response.cookies["csrftoken"].value
    signup = csrf_client.post(
        "/api/v1/auth/signup/",
        {
            "handle": "csrfpilot",
            "email": "csrfpilot@example.com",
            "password": "correct horse battery",
            "terms_accepted": True,
        },
        format="json",
        HTTP_X_CSRFTOKEN=token,
    )
    assert signup.status_code == 201

    response = csrf_client.post("/api/v1/auth/logout/", {}, format="json")

    assert response.status_code == 403
    assert response.json()["error"]["code"] in {"permission_denied", "csrf_failed", "authentication_required"}


@pytest.mark.django_db
def test_login_accepts_email_identifier(seeded, api_client):
    api_client.post(
        "/api/v1/auth/signup/",
        {
            "handle": "emailpilot",
            "email": "emailpilot@example.com",
            "password": "correct horse battery",
            "terms_accepted": True,
        },
        format="json",
    )
    api_client.post("/api/v1/auth/logout/", {}, format="json")

    response = api_client.post("/api/v1/auth/login/", {"identifier": "emailpilot@example.com", "password": "correct horse battery"}, format="json")

    assert response.status_code == 200
    assert response.json()["data"]["user"]["handle"] == "emailpilot"

