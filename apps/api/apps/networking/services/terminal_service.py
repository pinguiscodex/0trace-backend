import shlex

from apps.common.api.errors import GameAPIException
from apps.filesystem.models import FileNode
from apps.filesystem.services.file_service import create_node, update_file
from apps.filesystem.services.path_service import normalize_path
from apps.filesystem.services.permission_service import ensure_permission
from apps.networking.services.simulated_ssh_service import simulated_ssh_login
from apps.networking.services.terminal_history_service import append_terminal_history


def execute_terminal_command(*, user, machine, command: str):
    append_terminal_history(user=user, machine=machine, command=command)
    command = command.strip()
    if not command:
        return {"exit_code": 0, "stdout": "", "stderr": ""}

    os_style = machine.installed_os.os.terminal_style if hasattr(machine, "installed_os") and machine.installed_os else "windows-like"

    try:
        parts = shlex.split(command)
    except ValueError as exc:
        raise GameAPIException(str(exc), code="invalid_terminal_command", status_code=400) from exc
    name = parts[0].lower()

    if name in {"help", "man", "--help", "-h"}:
        return _help_command(os_style)

    if name in {"cls", "clear"}:
        return {"exit_code": 0, "stdout": "", "stderr": ""}

    if name == "ver":
        if os_style == "windows-like":
            os_name = machine.installed_os.os.name if hasattr(machine, "installed_os") and machine.installed_os else "DoorsOS"
            return {"exit_code": 0, "stdout": f"{os_name} Version 1.0", "stderr": ""}
        raise GameAPIException("Invalid terminal command.", code="invalid_terminal_command", status_code=400)

    if name == "uname":
        if os_style == "windows-like":
            raise GameAPIException("'uname' is not recognized. Use 'ver' on DoorsOS.", code="invalid_terminal_command", status_code=400)
        os_name = machine.installed_os.os.name if hasattr(machine, "installed_os") and machine.installed_os else "Unix"
        return {"exit_code": 0, "stdout": f"{os_name} 1.0 0trace x86_64", "stderr": ""}

    if name == "pwd":
        if os_style == "windows-like":
            raise GameAPIException("Invalid terminal command.", code="invalid_terminal_command", status_code=400)
        return {"exit_code": 0, "stdout": "/", "stderr": ""}

    if name in {"cd", "chdir"}:
        target = parts[1] if len(parts) > 1 else "/"
        normalized = normalize_path(target)
        try:
            FileNode.objects.get(machine=machine, path=normalized, kind=FileNode.Kind.DIRECTORY)
            display_path = normalized
            return {"exit_code": 0, "stdout": f"Changed directory to {display_path}", "stderr": ""}
        except FileNode.DoesNotExist:
            return {"exit_code": 1, "stdout": "", "stderr": f"{name}: {target}: No such directory"}

    if name in {"ls", "dir"}:
        path = normalize_path(parts[1] if len(parts) > 1 else "/")
        try:
            parent = FileNode.objects.get(machine=machine, path=path, kind=FileNode.Kind.DIRECTORY)
            ensure_permission(parent, user)
            children = list(parent.children.order_by("kind", "name"))
            if os_style == "windows-like":
                stdout = "\n".join(f"{c.name}{'/' if c.kind == FileNode.Kind.DIRECTORY else ''}" for c in children)
            else:
                stdout = "\n".join(c.name for c in children)
            return {"exit_code": 0, "stdout": stdout, "stderr": ""}
        except FileNode.DoesNotExist:
            return {"exit_code": 1, "stdout": "", "stderr": f"{name}: cannot access '{path}': No such file or directory"}

    if name in {"cat", "type"}:
        if len(parts) < 2:
            raise GameAPIException(f"{name} requires a path.", code="invalid_terminal_command")
        try:
            node = FileNode.objects.get(machine=machine, path=normalize_path(parts[1]), kind=FileNode.Kind.FILE)
            ensure_permission(node, user)
            return {"exit_code": 0, "stdout": node.content, "stderr": ""}
        except FileNode.DoesNotExist:
            return {"exit_code": 1, "stdout": "", "stderr": f"{name}: {parts[1]}: No such file or directory"}

    if name == "touch":
        if len(parts) < 2:
            raise GameAPIException("touch requires a path.", code="invalid_terminal_command")
        node = create_node(machine=machine, user=user, path=parts[1], kind=FileNode.Kind.FILE)
        return {"exit_code": 0, "stdout": f"created {node.path}", "stderr": ""}

    if name == "mkdir":
        if len(parts) < 2:
            raise GameAPIException("mkdir requires a path.", code="invalid_terminal_command")
        node = create_node(machine=machine, user=user, path=parts[1], kind=FileNode.Kind.DIRECTORY)
        return {"exit_code": 0, "stdout": f"created {node.path}", "stderr": ""}

    if name in {"rm", "del", "rmdir"}:
        args = [p for p in parts[1:] if not p.startswith("-")]
        if len(args) < 1:
            raise GameAPIException(f"{name} requires a path.", code="invalid_terminal_command")
        target_path = args[0]
        normalized = normalize_path(target_path)
        if normalized == "/" or target_path == "/":
            raise GameAPIException("Operation not permitted: cannot delete root directory.", code="permission_denied", status_code=403)
        try:
            node = FileNode.objects.get(machine=machine, path=normalized)
            ensure_permission(node, user, write=True)
            node.delete()
            return {"exit_code": 0, "stdout": f"deleted {target_path}", "stderr": ""}
        except FileNode.DoesNotExist:
            return {"exit_code": 1, "stdout": "", "stderr": f"{name}: {target_path}: No such file or directory"}

    if name == "nano":
        if len(parts) < 2:
            raise GameAPIException("nano requires a file path.", code="invalid_terminal_command")
        if os_style == "windows-like":
            raise GameAPIException("'nano' is not recognized as an internal or external command.", code="invalid_terminal_command", status_code=400)
        return _editor_command(machine=machine, user=user, editor="nano", parts=parts)

    if name == "notepad":
        if len(parts) < 2:
            raise GameAPIException("notepad requires a file path.", code="invalid_terminal_command")
        if os_style != "windows-like":
            raise GameAPIException("'notepad' is not available on this OS. Use 'nano'.", code="invalid_terminal_command", status_code=400)
        return _editor_command(machine=machine, user=user, editor="notepad", parts=parts)

    if name == "sudo":
        if os_style == "windows-like":
            raise GameAPIException("'sudo' is not recognized as an internal or external command.", code="invalid_terminal_command", status_code=400)
        if len(parts) < 2:
            raise GameAPIException("sudo requires a command.", code="invalid_terminal_command")
        return {"exit_code": 0, "stdout": f"[sudo] password for {user.handle}: Executing: {' '.join(parts[1:])}", "stderr": ""}

    if name in {"runas", "elevate"}:
        if os_style != "windows-like":
            raise GameAPIException(f"'{name}' is not available on this OS. Use 'sudo'.", code="invalid_terminal_command", status_code=400)
        if len(parts) < 2:
            raise GameAPIException(f"{name} requires a command.", code="invalid_terminal_command")
        return {"exit_code": 0, "stdout": f"[elevated] Executing as administrator: {' '.join(parts[1:])}", "stderr": ""}

    if name == "pacman":
        if os_style != "unix-like" or not _is_arcticos(machine):
            raise GameAPIException("'pacman' is not available on this OS.", code="invalid_terminal_command", status_code=400)
        if len(parts) < 2:
            raise GameAPIException("pacman requires options.", code="invalid_terminal_command")
        return {"exit_code": 0, "stdout": "pacman: package management.", "stderr": ""}

    if name in {"brew", "fruitpkg"}:
        if os_style != "macos-like" or not _is_fruitos(machine):
            raise GameAPIException(f"'{name}' is not available on this OS.", code="invalid_terminal_command", status_code=400)
        if len(parts) < 2:
            raise GameAPIException(f"{name} requires options.", code="invalid_terminal_command")
        return {"exit_code": 0, "stdout": f"{name}: package management.", "stderr": ""}

    if name in {"ipconfig", "ifconfig", "ip"}:
        if name == "ipconfig" and os_style != "windows-like":
            raise GameAPIException("'ipconfig' is not available on this OS. Use 'ifconfig' or 'ip'.", code="invalid_terminal_command", status_code=400)
        if name == "ifconfig" and os_style == "windows-like":
            raise GameAPIException("'ifconfig' is not available on this OS. Use 'ipconfig'.", code="invalid_terminal_command", status_code=400)
        if name == "ip" and os_style == "windows-like":
            raise GameAPIException("'ip' is not available on this OS. Use 'ipconfig'.", code="invalid_terminal_command", status_code=400)
        return {"exit_code": 0, "stdout": f"IP: {machine.fictional_ip}\nHostname: {machine.hostname}", "stderr": ""}

    if name == "ps":
        if os_style == "windows-like":
            raise GameAPIException("'ps' is not recognized. Use 'tasklist' on DoorsOS.", code="invalid_terminal_command", status_code=400)
        return {"exit_code": 0, "stdout": "PID   COMMAND\n1     init\n42    desktop\n128   terminal", "stderr": ""}

    if name == "tasklist":
        if os_style != "windows-like":
            raise GameAPIException("'tasklist' is not available on this OS.", code="invalid_terminal_command", status_code=400)
        return {"exit_code": 0, "stdout": "Image Name                     PID\n========================= ========\nSystem                           4\ndesktop.exe                    128\nterminal.exe                   256", "stderr": ""}

    if name == "kill":
        if os_style == "windows-like":
            raise GameAPIException("'kill' is not recognized. Use 'taskkill' on DoorsOS.", code="invalid_terminal_command", status_code=400)
        if len(parts) < 2:
            raise GameAPIException("kill requires a PID.", code="invalid_terminal_command")
        return {"exit_code": 0, "stdout": f"Process {parts[1]} terminated.", "stderr": ""}

    if name == "taskkill":
        if os_style != "windows-like":
            raise GameAPIException("'taskkill' is not available on this OS.", code="invalid_terminal_command", status_code=400)
        if len(parts) < 2:
            raise GameAPIException("taskkill requires a PID or image name.", code="invalid_terminal_command")
        return {"exit_code": 0, "stdout": f"Process {parts[1]} terminated.", "stderr": ""}

    if name == "apps":
        stdout = "\n".join(machine.app_installs.filter(active=True).values_list("app__slug", flat=True))
        return {"exit_code": 0, "stdout": stdout, "stderr": ""}

    if name == "sysinfo":
        os_name = machine.installed_os.os.name if hasattr(machine, "installed_os") and machine.installed_os else "Unknown"
        return {"exit_code": 0, "stdout": f"{machine.hostname} {machine.fictional_ip}\nOS: {os_name}", "stderr": ""}

    if name == "ssh":
        if len(parts) < 3:
            raise GameAPIException("ssh requires target IP and token.", code="invalid_terminal_command")
        session = simulated_ssh_login(actor=user, source_machine=machine, target_ip=parts[1], token=parts[2])
        return {"exit_code": 0, "stdout": f"connected:{session.id}", "stderr": ""}

    if name == "firewall":
        return {"exit_code": 0, "stdout": "Firewall: Active\nLevel: 3\nFailed attempts: 0", "stderr": ""}

    if name == "waterwall":
        return {"exit_code": 0, "stdout": "Waterwall: Active\nLevel: 2\nHistory: No attempts", "stderr": ""}

    if name in {"crack", "cracker"}:
        return {"exit_code": 0, "stdout": "Usage: crack <target_ip>\nStarts a password cracking job against the target IP.", "stderr": ""}

    if name in {"mine", "miner"}:
        return {"exit_code": 0, "stdout": "Usage: mine <coin> <cpu|gpu>\nStarts a crypto mining job.", "stderr": ""}

    if name == "webserver":
        return {"exit_code": 0, "stdout": "Webserver: Stopped\nNo website configured.", "stderr": ""}

    if name == "mail":
        return {"exit_code": 0, "stdout": "Mail: 0 unread messages.", "stderr": ""}

    if name == "whoami":
        return {"exit_code": 0, "stdout": user.handle, "stderr": ""}

    if name == "hostname":
        return {"exit_code": 0, "stdout": machine.hostname, "stderr": ""}

    if name == "date":
        from django.utils import timezone
        return {"exit_code": 0, "stdout": timezone.now().strftime("%Y-%m-%d %H:%M:%S"), "stderr": ""}

    if name == "uptime":
        return {"exit_code": 0, "stdout": f"up 1 day, 2:34, 1 user", "stderr": ""}

    if name == "echo":
        return _echo_command(machine=machine, user=user, parts=parts)

    raise GameAPIException(f"'{name}' is not recognized as a command.", code="invalid_terminal_command", status_code=400)


def _echo_command(*, machine, user, parts):
    if ">" in parts or ">>" in parts:
        append = ">>" in parts
        operator = ">>" if append else ">"
        operator_index = parts.index(operator)
        if operator_index == 1 or operator_index == len(parts) - 1:
            raise GameAPIException("echo redirection requires text and a file path.", code="invalid_terminal_command")
        content = " ".join(parts[1:operator_index])
        path = parts[operator_index + 1]
        node = _write_terminal_file(machine=machine, user=user, path=path, content=content, append=append)
        return {"exit_code": 0, "stdout": f"wrote {node.path}", "stderr": ""}
    return {"exit_code": 0, "stdout": " ".join(parts[1:]), "stderr": ""}


def _editor_command(*, machine, user, editor: str, parts):
    path = parts[1]
    if len(parts) == 2:
        node = _get_or_create_terminal_file(machine=machine, user=user, path=path)
        return {
            "exit_code": 0,
            "stdout": f"{editor}: {node.path}\n{node.content}",
            "stderr": "",
        }

    mode = parts[2]
    if mode not in {"--write", "--append"}:
        raise GameAPIException(
            f"{editor} supports: {editor} <path>, {editor} <path> --write <text>, {editor} <path> --append <text>.",
            code="invalid_terminal_command",
        )
    if len(parts) < 4:
        raise GameAPIException(f"{editor} {mode} requires text.", code="invalid_terminal_command")
    node = _write_terminal_file(
        machine=machine,
        user=user,
        path=path,
        content=" ".join(parts[3:]),
        append=mode == "--append",
    )
    action = "appended" if mode == "--append" else "wrote"
    return {"exit_code": 0, "stdout": f"{action} {node.path}", "stderr": ""}


def _get_or_create_terminal_file(*, machine, user, path: str):
    normalized = normalize_path(path)
    node = FileNode.objects.filter(machine=machine, path=normalized).first()
    if node is None:
        return create_node(machine=machine, user=user, path=normalized, kind=FileNode.Kind.FILE)
    if node.kind != FileNode.Kind.FILE:
        raise GameAPIException("Cannot edit a directory.", code="validation_error")
    ensure_permission(node, user)
    return node


def _write_terminal_file(*, machine, user, path: str, content: str, append: bool = False):
    node = _get_or_create_terminal_file(machine=machine, user=user, path=path)
    next_content = f"{node.content}{content}" if append else content
    return update_file(node=node, user=user, content=next_content)


def _help_command(os_style: str):
    if os_style == "windows-like":
        commands = (
            "Available DoorsOS commands:\n"
            "  dir        - List directory contents\n"
            "  cd         - Change directory\n"
            "  type       - Display file contents\n"
            "  mkdir      - Create a directory\n"
            "  del        - Delete a file\n"
            "  rmdir      - Remove a directory\n"
            "  cls        - Clear screen\n"
            "  ver        - Show OS version\n"
            "  ipconfig   - Show network configuration\n"
            "  tasklist   - List running processes\n"
            "  sysinfo    - Show system information\n"
            "  apps       - List installed apps\n"
            "  whoami     - Show current user\n"
            "  hostname   - Show hostname\n"
            "  date       - Show current date/time\n"
            "  echo       - Print text\n"
            "  firewall   - Show firewall status\n"
            "  waterwall  - Show waterwall status\n"
            "  crack      - Start password cracking\n"
            "  mine       - Start crypto mining\n"
            "  webserver  - Show webserver status\n"
            "  mail       - Show mail status\n"
            "  ssh        - Connect to another machine\n"
            "  help       - Show this help"
        )
    elif os_style == "macos-like":
        commands = (
            "Available FruitOS commands:\n"
            "  ls         - List directory contents\n"
            "  cd         - Change directory\n"
            "  cat        - Display file contents\n"
            "  nano       - Edit files\n"
            "  sudo       - Execute with elevated privileges\n"
            "  mkdir      - Create a directory\n"
            "  rm         - Remove files/directories\n"
            "  clear      - Clear screen\n"
            "  pwd        - Print working directory\n"
            "  ifconfig   - Show network configuration\n"
            "  ps         - List running processes\n"
            "  sysinfo    - Show system information\n"
            "  apps       - List installed apps\n"
            "  whoami     - Show current user\n"
            "  hostname   - Show hostname\n"
            "  date       - Show current date/time\n"
            "  uptime     - Show system uptime\n"
            "  echo       - Print text\n"
            "  firewall   - Show firewall status\n"
            "  waterwall  - Show waterwall status\n"
            "  crack      - Start password cracking\n"
            "  mine       - Start crypto mining\n"
            "  webserver  - Show webserver status\n"
            "  mail       - Show mail status\n"
            "  ssh        - Connect to another machine\n"
            "  help       - Show this help"
        )
    elif os_style == "unix-like":
        commands = (
            "Available ArcticOS commands:\n"
            "  ls         - List directory contents\n"
            "  cd         - Change directory\n"
            "  cat        - Display file contents\n"
            "  nano       - Edit files\n"
            "  sudo       - Execute with elevated privileges\n"
            "  pacman     - Package manager\n"
            "  mkdir      - Create a directory\n"
            "  rm         - Remove files/directories\n"
            "  clear      - Clear screen\n"
            "  pwd        - Print working directory\n"
            "  ip         - Show network configuration\n"
            "  ps         - List running processes\n"
            "  sysinfo    - Show system information\n"
            "  apps       - List installed apps\n"
            "  whoami     - Show current user\n"
            "  hostname   - Show hostname\n"
            "  date       - Show current date/time\n"
            "  uptime     - Show system uptime\n"
            "  echo       - Print text\n"
            "  firewall   - Show firewall status\n"
            "  waterwall  - Show waterwall status\n"
            "  crack      - Start password cracking\n"
            "  mine       - Start crypto mining\n"
            "  webserver  - Show webserver status\n"
            "  mail       - Show mail status\n"
            "  ssh        - Connect to another machine\n"
            "  help       - Show this help"
        )
    else:
        commands = "Available commands: help, ls/dir, cat/type, mkdir, rm/del, clear/cls, sysinfo, apps, whoami, hostname, date, echo, ssh, help"
    return {"exit_code": 0, "stdout": commands, "stderr": ""}


def _is_arcticos(machine) -> bool:
    if hasattr(machine, "installed_os") and machine.installed_os:
        return machine.installed_os.os.slug == "arcticos"
    return False


def _is_fruitos(machine) -> bool:
    if hasattr(machine, "installed_os") and machine.installed_os:
        return machine.installed_os.os.slug == "fruitos"
    return False
