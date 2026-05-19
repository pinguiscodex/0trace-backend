import pytest

from apps.accounts.models import User
from apps.browser.services.browser_resolution_service import resolve_url
from apps.common.api.errors import GameAPIException
from apps.filesystem.models import FileNode
from apps.machines.services.machine_bootstrap_service import bootstrap_machine_for_user
from apps.networking.services.terminal_service import execute_terminal_command


@pytest.mark.django_db
def test_terminal_rejects_host_shell_commands(seeded):
    user = User.objects.create_user("termuser", "term@example.com", "correct horse battery", display_name="Term")
    machine = bootstrap_machine_for_user(user)

    with pytest.raises(GameAPIException):
        execute_terminal_command(user=user, machine=machine, command="rm -rf /")

    assert execute_terminal_command(user=user, machine=machine, command="sysinfo")["stdout"].startswith(machine.hostname)


@pytest.mark.django_db
def test_browser_resolve_only_returns_seeded_ingame_sites(seeded):
    resolved = resolve_url("https://www.microhard.com")

    assert resolved["site_type"] == "predefined"
    assert resolved["sandbox_policy"]["external_fetch"] is False
    assert resolve_url("https://www.external-example.invalid") is None


@pytest.mark.django_db
def test_terminal_can_write_and_append_files_with_redirection(seeded):
    user = User.objects.create_user("writer", "writer@example.com", "correct horse battery", display_name="Writer")
    machine = bootstrap_machine_for_user(user)

    result = execute_terminal_command(user=user, machine=machine, command="echo alpha > /notes.txt")
    assert result["exit_code"] == 0

    execute_terminal_command(user=user, machine=machine, command="echo beta >> /notes.txt")

    node = FileNode.objects.get(machine=machine, path="/notes.txt")
    assert node.content == "alphabeta"
    assert execute_terminal_command(user=user, machine=machine, command="type /notes.txt")["stdout"] == "alphabeta"


@pytest.mark.django_db
def test_terminal_notepad_write_updates_file_content(seeded):
    user = User.objects.create_user("noter", "noter@example.com", "correct horse battery", display_name="Noter")
    machine = bootstrap_machine_for_user(user)

    result = execute_terminal_command(user=user, machine=machine, command='notepad /todo.txt --write "ship the build"')

    assert result["stdout"] == "wrote /todo.txt"
    assert FileNode.objects.get(machine=machine, path="/todo.txt").content == "ship the build"
