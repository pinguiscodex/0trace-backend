from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.response import Response


def ok(data: Any, *, status_code: int = status.HTTP_200_OK) -> Response:
    return Response({"data": data}, status=status_code)


def created(data: Any) -> Response:
    return ok(data, status_code=status.HTTP_201_CREATED)


def accepted(data: Any, *, request_id: str = "", status_text: str = "accepted") -> Response:
    return Response({"data": data, "meta": {"request_id": request_id, "status": status_text}}, status=status.HTTP_202_ACCEPTED)


def no_content() -> Response:
    return Response(status=status.HTTP_204_NO_CONTENT)

