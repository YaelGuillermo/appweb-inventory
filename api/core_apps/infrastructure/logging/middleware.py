# api/core_apps/infrastructure/logging/middleware.py
from __future__ import annotations

import logging
import time

from django.conf import settings

logger = logging.getLogger("api.http")


class HttpRequestLoggingMiddleware:
    """Small HTTP access logger with snake_case structured fields."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, "HTTP_REQUEST_LOGGING_ENABLED", True):
            return self.get_response(request)

        started_at = time.perf_counter()
        response = self.get_response(request)
        latency_ms = round((time.perf_counter() - started_at) * 1000)
        request_id = getattr(request, "request_id", "")
        remote_addr = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get(
            "REMOTE_ADDR", ""
        )

        logger.info(
            "method=%s path=%s status_code=%s latency_ms=%s request_id=%s remote_addr=%s",
            request.method,
            request.get_full_path(),
            getattr(response, "status_code", None),
            latency_ms,
            request_id,
            remote_addr,
            extra={
                "method": request.method,
                "path": request.get_full_path(),
                "status_code": getattr(response, "status_code", None),
                "latency_ms": latency_ms,
                "request_id": request_id,
                "remote_addr": remote_addr,
            },
        )
        return response
