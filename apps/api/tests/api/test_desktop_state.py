import pytest

from apps.machines.models import DesktopWindowState, Machine


@pytest.mark.django_db
def test_desktop_state_included_in_bootstrap(seeded, api_client):
    api_client.post(
        "/api/v1/auth/signup/",
        {
            "handle": "desktest",
            "email": "desktest@example.com",
            "password": "correct horse battery",
            "terms_accepted": True,
        },
        format="json",
    )

    response = api_client.get("/api/v1/bootstrap/")

    assert response.status_code == 200
    data = response.json()["data"]
    assert "desktopWindowState" in data
    assert data["desktopWindowState"]["windows"] == {}
    assert data["desktopWindowState"]["activeWindowId"] is None
    assert data["desktopWindowState"]["zSeed"] == 0


@pytest.mark.django_db
def test_get_desktop_state_returns_defaults(seeded, api_client):
    api_client.post(
        "/api/v1/auth/signup/",
        {
            "handle": "getstate",
            "email": "getstate@example.com",
            "password": "correct horse battery",
            "terms_accepted": True,
        },
        format="json",
    )

    bootstrap = api_client.get("/api/v1/bootstrap/").json()["data"]
    machine_id = bootstrap["active_machine"]["id"]

    response = api_client.get(f"/api/v1/machines/{machine_id}/desktop-state/")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["windows"] == {}
    assert data["active_window_id"] is None
    assert data["z_seed"] == 0


@pytest.mark.django_db
def test_put_desktop_state_persists(seeded, api_client):
    api_client.post(
        "/api/v1/auth/signup/",
        {
            "handle": "putstate",
            "email": "putstate@example.com",
            "password": "correct horse battery",
            "terms_accepted": True,
        },
        format="json",
    )

    bootstrap = api_client.get("/api/v1/bootstrap/").json()["data"]
    machine_id = bootstrap["active_machine"]["id"]

    payload = {
        "windows": {
            "win-terminal-1": {
                "id": "win-terminal-1",
                "appId": "terminal",
                "title": "Terminal",
                "status": "open",
                "bounds": {"x": 100, "y": 50, "width": 800, "height": 600},
                "previousBounds": None,
                "zIndex": 1,
                "dirty": False,
            }
        },
        "active_window_id": "win-terminal-1",
        "z_seed": 42,
    }

    response = api_client.put(f"/api/v1/machines/{machine_id}/desktop-state/", payload, format="json")

    assert response.status_code == 200
    data = response.json()["data"]
    assert "win-terminal-1" in data["windows"]
    assert data["active_window_id"] == "win-terminal-1"
    assert data["z_seed"] == 42

    machine = Machine.objects.get(id=machine_id)
    state = DesktopWindowState.objects.get(machine=machine)
    assert "win-terminal-1" in state.windows
    assert state.active_window_id == "win-terminal-1"
    assert state.z_seed == 42


@pytest.mark.django_db
def test_desktop_state_survives_bootstrap_after_update(seeded, api_client):
    api_client.post(
        "/api/v1/auth/signup/",
        {
            "handle": "survive",
            "email": "survive@example.com",
            "password": "correct horse battery",
            "terms_accepted": True,
        },
        format="json",
    )

    bootstrap = api_client.get("/api/v1/bootstrap/").json()["data"]
    machine_id = bootstrap["active_machine"]["id"]

    api_client.put(
        f"/api/v1/machines/{machine_id}/desktop-state/",
        {
            "windows": {"win-test": {"id": "win-test", "appId": "terminal", "status": "open"}},
            "active_window_id": "win-test",
            "z_seed": 99,
        },
        format="json",
    )

    response = api_client.get("/api/v1/bootstrap/")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "win-test" in data["desktopWindowState"]["windows"]
    assert data["desktopWindowState"]["activeWindowId"] == "win-test"
    assert data["desktopWindowState"]["zSeed"] == 99
