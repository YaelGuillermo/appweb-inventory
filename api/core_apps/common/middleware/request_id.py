from __future__ import annotations

from uuid import uuid4

REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"
RESPONSE_REQUEST_ID_HEADER = "X-Request-Id"


class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        incoming_request_id = request.META.get(REQUEST_ID_HEADER)
        request.request_id = incoming_request_id or str(uuid4())

        response = self.get_response(request)
        response[RESPONSE_REQUEST_ID_HEADER] = request.request_id

        return response
