# api/core_apps/common/exceptions/base.py
from __future__ import annotations

from typing import Any, Literal

from rest_framework import status
from rest_framework.exceptions import APIException

ErrorKind = Literal["field", "business", "system"]


class AppAPIException(APIException):
    """
    Domain-level API exception for predictable business errors.

    Use this when a service or view needs to raise an error that should be
    rendered by the global exception handler using the same response envelope.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Application error."
    default_code = "application_error"
    error_path = "general"
    error_kind: ErrorKind = "business"

    def __init__(
        self,
        detail: str | None = None,
        *,
        code: str | None = None,
        status_code: int | None = None,
        errors: dict[str, Any] | None = None,
        error_path: str | None = None,
        error_kind: ErrorKind | None = None,
        message: dict[str, Any] | None = None,
        limits: dict[str, Any] | None = None,
    ) -> None:
        if status_code is not None:
            self.status_code = status_code

        self.error_code = code or self.default_code
        self.errors = errors
        self.error_path = error_path or self.error_path
        self.error_kind = error_kind or self.error_kind
        self.message = message
        self.limits = limits

        super().__init__(detail=detail or self.default_detail, code=self.error_code)
