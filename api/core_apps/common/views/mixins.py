from __future__ import annotations

from typing import Any

from rest_framework.response import Response

from core_apps.common.responses.messages import ResponseMessage


class ApiResponseMixin:
    response_messages: dict[str, ResponseMessage] = {}

    def get_response_message(self, action: str | None = None) -> dict[str, Any] | None:
        action = action or getattr(self, "action", None)
        message = self.response_messages.get(action or "")
        return message.to_dict() if message else None

    def success_response(
        self,
        data: Any = None,
        *,
        status: int = 200,
        message: ResponseMessage | dict | None = None,
        pagination: dict | None = None,
        links: dict | None = None,
        limits: dict | None = None,
    ) -> Response:
        response = Response({"data": data}, status=status)
        response.message = self._resolve_message(message)
        response.pagination = pagination
        response.links = links
        response.limits = limits
        return response

    def _resolve_message(self, message: ResponseMessage | dict | None):
        if isinstance(message, ResponseMessage):
            return message.to_dict()

        if isinstance(message, dict):
            return message

        return self.get_response_message()
