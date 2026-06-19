from __future__ import annotations

import math
from typing import Any

from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core_apps.common.responses.hateoas import build_page_url


class CustomPageNumberPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "page_size"

    def get_page_size(self, request):
        page_size = super().get_page_size(request)
        default_page_size = getattr(settings, "REST_PAGINATION_PAGE_SIZE", 20)
        return page_size or default_page_size

    def get_paginated_response(self, data: list[Any]) -> Response:
        request_path = self.request.get_full_path()
        page_size = self.get_page_size(self.request)
        total_items = self.page.paginator.count
        total_pages = max(1, math.ceil(total_items / page_size))
        current_page = self.page.number

        pagination = {
            "meta": {
                "current_page": current_page,
                "total_pages": total_pages,
                "total_items": total_items,
                "page_size": page_size,
                "count": len(data),
            },
            "links": {
                "previous": self.get_previous_link(),
                "next": self.get_next_link(),
                "first": build_page_url(request_path, 1, page_size),
                "last": build_page_url(request_path, total_pages, page_size),
            },
        }

        response = Response({"data": data, "pagination": pagination})
        response.pagination = pagination
        return response
