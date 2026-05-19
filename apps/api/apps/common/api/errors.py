from __future__ import annotations

from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, NotAuthenticated, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


class GameAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Request could not be processed."
    default_code = "validation_error"

    def __init__(
        self,
        message: str | None = None,
        *,
        code: str | None = None,
        status_code: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(detail=message or self.default_detail, code=code or self.default_code)
        if status_code is not None:
            self.status_code = status_code
        self.details = details or {}


def request_id_from_context(context: dict[str, Any]) -> str:
    request = context.get("request")
    return getattr(request, "request_id", "") if request is not None else ""


def error_payload(code: str, message: str, *, request_id: str = "", details: Any | None = None) -> dict[str, Any]:
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
            "request_id": request_id,
        }
    }


def exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    request_id = request_id_from_context(context)

    if isinstance(exc, (Http404, ObjectDoesNotExist)):
        return Response(error_payload("not_found", "Resource not found.", request_id=request_id), status=404)

    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    code = "internal_error"
    message = "Unexpected error."
    details: Any = {}

    if isinstance(exc, NotAuthenticated):
        code = "authentication_required"
        message = "Authentication is required."
    elif isinstance(exc, PermissionDenied):
        code = "permission_denied"
        message = "You do not have permission to perform this action."
    elif isinstance(exc, ValidationError):
        code = "validation_error"
        message = "Validation failed."
        details = response.data
    elif isinstance(exc, GameAPIException):
        code = str(exc.get_codes()) if exc.get_codes() else exc.default_code
        message = str(exc.detail)
        details = getattr(exc, "details", {})
    else:
        detail = response.data.get("detail") if isinstance(response.data, dict) else response.data
        if detail:
            message = str(detail)
            if hasattr(exc, "get_codes"):
                raw_code = exc.get_codes()
                code = raw_code if isinstance(raw_code, str) else "validation_error"

    response.data = error_payload(code, message, request_id=request_id, details=details)
    return response
