from apps.common.api.errors import GameAPIException


def normalize_path(path: str) -> str:
    if not path:
        raise GameAPIException("Path is required.", code="validation_error")
    if "\x00" in path:
        raise GameAPIException("Path contains invalid characters.", code="validation_error")
    parts = []
    for part in path.replace("\\", "/").split("/"):
        if part in {"", "."}:
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return "/" + "/".join(parts) if parts else "/"


def parent_path(path: str) -> str | None:
    path = normalize_path(path)
    if path == "/":
        return None
    parent = path.rsplit("/", 1)[0]
    return parent or "/"


def basename(path: str) -> str:
    path = normalize_path(path)
    if path == "/":
        return "/"
    return path.rsplit("/", 1)[1]

