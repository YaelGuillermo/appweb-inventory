from __future__ import annotations

from typing import Any

from rest_framework.renderers import JSONRenderer

from core_apps.common.responses.envelope import (
    build_error_envelope,
    build_success_envelope,
)


class CustomJSONRenderer(JSONRenderer):
    """
    Unified JSON renderer for the API.

    All response keys are snake_case:
    status, status_code, path, message, data, pagination, links, limits, meta,
    timestamp.
    """

    charset = "utf-8"

    def render(
        self,
        data: Any,
        accepted_media_type: str | None = None,
        renderer_context: dict | None = None,
    ) -> bytes:
        renderer_context = renderer_context or {}
        response = renderer_context.get("response")
        request = renderer_context.get("request")

        if response is None or getattr(response, "skip_envelope", False):
            return super().render(data, accepted_media_type, renderer_context)

        if self._is_already_wrapped(data):
            return super().render(data, accepted_media_type, renderer_context)

        status_code = int(getattr(response, "status_code", 200))
        is_error = bool(getattr(response, "exception", False)) or status_code >= 400

        if is_error:
            envelope = build_error_envelope(
                data=data,
                request=request,
                status_code=status_code,
                message=getattr(response, "message", None),
                errors=getattr(response, "errors", None),
            )
        else:
            normalized = self._normalize_success_data(data)
            envelope = build_success_envelope(
                data=normalized["data"],
                request=request,
                status_code=status_code,
                message=getattr(response, "message", None) or normalized.get("message"),
                pagination=getattr(response, "pagination", None)
                or normalized.get("pagination"),
                links=getattr(response, "links", None) or normalized.get("links"),
                limits=getattr(response, "limits", None) or normalized.get("limits"),
            )

        return super().render(envelope, accepted_media_type, renderer_context)

    def _is_already_wrapped(self, data: Any) -> bool:
        return (
            isinstance(data, dict)
            and "status" in data
            and "status_code" in data
            and "data" in data
            and "timestamp" in data
        )

    def _normalize_success_data(self, data: Any) -> dict[str, Any]:
        if not isinstance(data, dict):
            return {"data": data}

        if "data" in data:
            return {
                "data": data.get("data"),
                "message": data.get("message"),
                "pagination": data.get("pagination"),
                "links": data.get("links"),
                "limits": data.get("limits"),
            }

        if "results" in data:
            return {
                "data": data.get("results"),
                "pagination": data.get("pagination"),
                "links": data.get("links"),
                "limits": data.get("limits"),
            }

        return {"data": data}
