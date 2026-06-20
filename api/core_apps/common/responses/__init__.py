# api/core_apps/common/responses/__init__.py
from .envelope import build_error_envelope, build_success_envelope
from .errors import (
    GENERAL_ERROR_PATH,
    SYSTEM_ERROR_PATH,
    append_business_failure,
    append_failure,
    append_field_failure,
    append_system_failure,
    extract_limits,
    normalize_errors,
)
from .hateoas import (
    build_base_links,
    build_collection_links,
    build_detail_links,
    build_link,
    build_page_url,
    merge_links,
    strip_query,
)
from .messages import ResponseMessage, get_default_message

__all__ = [
    "GENERAL_ERROR_PATH",
    "SYSTEM_ERROR_PATH",
    "ResponseMessage",
    "append_business_failure",
    "append_failure",
    "append_field_failure",
    "append_system_failure",
    "build_base_links",
    "build_collection_links",
    "build_detail_links",
    "build_error_envelope",
    "build_link",
    "build_page_url",
    "build_success_envelope",
    "extract_limits",
    "get_default_message",
    "merge_links",
    "normalize_errors",
    "strip_query",
]
