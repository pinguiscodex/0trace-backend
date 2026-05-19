from apps.filesystem.models import FileNode


def append_terminal_history(*, user, machine, command: str, max_lines=100):
    """Append a command to the terminal history file."""
    try:
        history_file = FileNode.objects.get(
            machine=machine,
            path="/home/.terminal_history",
            owner=user,
        )
        content = history_file.content or ""
        lines = [line for line in content.splitlines() if line.strip()]
        lines.append(command)
        if len(lines) > max_lines:
            lines = lines[-max_lines:]
        history_file.content = "\n".join(lines) + "\n"
        history_file.save(update_fields=["content"])
    except FileNode.DoesNotExist:
        try:
            home_dir = FileNode.objects.get(machine=machine, path="/home", kind=FileNode.Kind.DIRECTORY)
        except FileNode.DoesNotExist:
            home_dir = None
        FileNode.objects.create(
            machine=machine,
            path="/home/.terminal_history",
            name=".terminal_history",
            kind=FileNode.Kind.FILE,
            owner=user,
            parent=home_dir,
            content=command + "\n",
            is_hidden=True,
        )


def get_terminal_history(user, machine, limit=50):
    """Retrieve recent terminal command history for a machine.
    
    Reads from the machine's terminal history file stored in the filesystem.
    Returns a list of command strings.
    """
    try:
        history_file = FileNode.objects.get(
            machine=machine,
            path="/home/.terminal_history",
            owner=user,
        )
        content = history_file.content or ""
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        return lines[-limit:]
    except FileNode.DoesNotExist:
        return []
