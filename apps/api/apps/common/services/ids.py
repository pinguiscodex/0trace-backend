import uuid


def new_uuid() -> uuid.UUID:
    return uuid.uuid4()


def short_code(prefix: str = "") -> str:
    value = uuid.uuid4().hex[:12]
    return f"{prefix}{value}" if prefix else value

