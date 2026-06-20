# api/core_apps/common/responses/envelope.py
from __future__ import annotations

from typing import Any
from uuid import uuid4

from django.conf import settings
from django.utils import timezone

from core_apps.common.responses.errors import normalize_errors
from core_apps.common.responses.hateoas import build_base_links, merge_links
from core_apps.common.responses.messages import get_default_message


def get_request_path(request) -> str:
    if request is None:
        return ""

    return request.get_full_path()


def get_request_id(request) -> str:
    return getattr(request, "request_id", None) or str(uuid4())


def get_locale(request) -> str:
    return getattr(request, "LANGUAGE_CODE", None) or getattr(
        settings,
        "LANGUAGE_CODE",
        "en-us",
    )


def build_meta(request) -> dict[str, Any]:
    return {
        "api_version": getattr(settings, "API_VERSION", "v1"),
        "environment": getattr(settings, "ENVIRONMENT", "development"),
        "request_id": get_request_id(request),
        "locale": get_locale(request),
    }


def build_success_envelope(
    *,
    data: Any,
    request,
    status_code: int,
    message: dict | None = None,
    pagination: dict | None = None,
    links: dict | None = None,
    limits: dict | None = None,
) -> dict[str, Any]:
    path = get_request_path(request)
    payload = {
        "status": True,
        "status_code": status_code,
        "path": path,
        "message": message or get_default_message(status_code, is_error=False),
        "data": data,
        "links": merge_links(build_base_links(path), links),
        "meta": build_meta(request),
        "timestamp": timezone.now().isoformat(),
    }

    if pagination:
        payload["pagination"] = pagination

    if limits:
        payload["limits"] = limits

    return payload


def build_error_envelope(
    *,
    data: Any,
    request,
    status_code: int,
    message: dict | None = None,
    errors: dict | None = None,
    limits: dict | None = None,
) -> dict[str, Any]:
    normalized_errors = errors or normalize_errors(data, status_code=status_code)

    payload = {
        "status": False,
        "status_code": status_code,
        "path": get_request_path(request),
        "message": message or get_default_message(status_code, is_error=True),
        "data": None,
        "meta": build_meta(request),
        "timestamp": timezone.now().isoformat(),
    }

    if normalized_errors:
        payload["errors"] = normalized_errors

    if limits:
        payload["limits"] = limits

    return payload
