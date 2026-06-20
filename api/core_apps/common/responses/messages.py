# api/core_apps/common/responses/messages.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.utils.translation import gettext as _

DEFAULT_SUCCESS_DURATION_MS = 4500
DEFAULT_ERROR_DURATION_MS = 5000


@dataclass(frozen=True, slots=True)
class ResponseMessage:
    title: str
    description: str
    duration_ms: int = DEFAULT_SUCCESS_DURATION_MS
    translate: bool = True

    def to_dict(self) -> dict[str, Any]:
        title = _(self.title) if self.translate else self.title
        description = _(self.description) if self.translate else self.description

        return {
            "title": str(title),
            "description": str(description),
            "duration_ms": self.duration_ms,
        }


SUCCESS_MESSAGES: dict[int, ResponseMessage] = {
    200: ResponseMessage(
        title="Operation completed",
        description="The operation was completed successfully.",
    ),
    201: ResponseMessage(
        title="Record created",
        description="The record was created successfully.",
    ),
    204: ResponseMessage(
        title="Record deleted",
        description="The record was deleted successfully.",
    ),
}

ERROR_MESSAGES: dict[int, ResponseMessage] = {
    400: ResponseMessage(
        title="Invalid request",
        description="Review the submitted data and try again.",
        duration_ms=DEFAULT_ERROR_DURATION_MS,
    ),
    401: ResponseMessage(
        title="Authentication required",
        description="You must sign in to continue.",
        duration_ms=DEFAULT_ERROR_DURATION_MS,
    ),
    403: ResponseMessage(
        title="Access denied",
        description="You do not have permission to perform this action.",
        duration_ms=DEFAULT_ERROR_DURATION_MS,
    ),
    404: ResponseMessage(
        title="Resource not found",
        description="The requested resource does not exist or is not available.",
        duration_ms=DEFAULT_ERROR_DURATION_MS,
    ),
    405: ResponseMessage(
        title="Method not allowed",
        description="This HTTP method is not allowed for this resource.",
        duration_ms=DEFAULT_ERROR_DURATION_MS,
    ),
    409: ResponseMessage(
        title="Conflict",
        description="The request conflicts with the current state of the resource.",
        duration_ms=DEFAULT_ERROR_DURATION_MS,
    ),
    415: ResponseMessage(
        title="Unsupported media type",
        description="The submitted content type is not supported.",
        duration_ms=DEFAULT_ERROR_DURATION_MS,
    ),
    429: ResponseMessage(
        title="Too many requests",
        description="You have made too many requests. Try again later.",
        duration_ms=DEFAULT_ERROR_DURATION_MS,
    ),
    500: ResponseMessage(
        title="Internal error",
        description="An unexpected error occurred.",
        duration_ms=DEFAULT_ERROR_DURATION_MS,
    ),
}


def get_default_message(status_code: int, *, is_error: bool) -> dict[str, Any]:
    messages = ERROR_MESSAGES if is_error else SUCCESS_MESSAGES
    fallback = ERROR_MESSAGES[500] if is_error else SUCCESS_MESSAGES[200]
    return messages.get(status_code, fallback).to_dict()
