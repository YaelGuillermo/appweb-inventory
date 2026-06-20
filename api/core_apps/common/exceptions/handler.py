# api/core_apps/common/exceptions/handler.py
from __future__ import annotations

import logging
from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from core_apps.common.exceptions.base import AppAPIException
from core_apps.common.responses.errors import (
    append_business_failure,
    append_system_failure,
    extract_limits,
    get_default_error_code,
    normalize_errors,
)
from core_apps.common.responses.messages import get_default_message

logger = logging.getLogger(__name__)


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """
    Global DRF exception handler.

    This is the Django/DRF equivalent of a NestJS HTTP exception filter.
    It does not render the final envelope directly; it normalizes message,
    errors and limits, then lets CustomJSONRenderer produce the final JSON.
    """

    exc = normalize_django_validation_error(exc)
    response = drf_exception_handler(exc, context)

    if response is None:
        return build_unhandled_exception_response(exc, context)

    status_code = int(response.status_code)
    original_data = response.data
    custom_errors = getattr(exc, "errors", None)
    custom_message = getattr(exc, "message", None)
    custom_limits = getattr(exc, "limits", None)

    response.exception = True
    response.message = custom_message or get_default_message(status_code, is_error=True)
    response.errors = custom_errors or normalize_errors(
        original_data,
        status_code=status_code,
        default_code=get_default_error_code(status_code),
    )
    response.limits = custom_limits or extract_limits(original_data)
    response.data = None

    return response


def normalize_django_validation_error(exc: Exception) -> Exception:
    if not isinstance(exc, DjangoValidationError):
        return exc

    if hasattr(exc, "message_dict"):
        return DRFValidationError(exc.message_dict)

    if hasattr(exc, "messages"):
        return DRFValidationError(exc.messages)

    return DRFValidationError(str(exc))


def build_unhandled_exception_response(
    exc: Exception,
    context: dict[str, Any],
) -> Response:
    status_code = resolve_status_code(exc) or status.HTTP_500_INTERNAL_SERVER_ERROR
    response = Response(None, status=status_code)
    response.exception = True
    response.message = getattr(exc, "message", None) or get_default_message(
        status_code,
        is_error=True,
    )
    response.limits = getattr(exc, "limits", None)

    if isinstance(exc, AppAPIException) and exc.errors:
        response.errors = exc.errors
        return response

    if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        log_unhandled_exception(exc, context)
        response.errors = append_system_failure(
            {},
            value="An unexpected error occurred.",
            fallback_code=get_default_error_code(status_code),
        )
        return response

    response.errors = append_business_failure(
        {},
        value=str(exc),
        fallback_code=get_default_error_code(status_code),
    )
    return response


def resolve_status_code(exc: Exception) -> int | None:
    candidate = getattr(exc, "status_code", None) or getattr(exc, "status", None)

    if not isinstance(candidate, int):
        return None

    if candidate < 400 or candidate > 599:
        return None

    return candidate


def log_unhandled_exception(exc: Exception, context: dict[str, Any]) -> None:
    request = context.get("request")

    if request is None:
        logger.error(
            "Unhandled API exception", exc_info=(type(exc), exc, exc.__traceback__)
        )
        return

    method = getattr(request, "method", "UNKNOWN")
    path = request.get_full_path() if hasattr(request, "get_full_path") else ""
    logger.error(
        "Unhandled API exception on %s %s",
        method,
        path,
        exc_info=(type(exc), exc, exc.__traceback__),
    )
