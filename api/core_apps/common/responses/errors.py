# api/core_apps/common/responses/errors.py
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal

from rest_framework.exceptions import ErrorDetail

ErrorKind = Literal["field", "business", "system"]

GENERAL_ERROR_PATH = "general"
SYSTEM_ERROR_PATH = "system"
NON_FIELD_ERRORS_KEY = "non_field_errors"
ERROR_METADATA_KEYS = {"code", "status", "status_code", "limits"}


def get_default_error_code(status_code: int | None = None) -> str:
    default_codes = {
        400: "bad_request",
        401: "not_authenticated",
        403: "permission_denied",
        404: "not_found",
        405: "method_not_allowed",
        409: "conflict",
        415: "unsupported_media_type",
        429: "throttled",
        500: "internal_server_error",
    }
    return default_codes.get(status_code or 500, "error")


def get_default_error_kind(status_code: int | None = None) -> ErrorKind:
    return "system" if status_code and status_code >= 500 else "business"


def get_default_error_path(status_code: int | None = None) -> str:
    return (
        SYSTEM_ERROR_PATH if status_code and status_code >= 500 else GENERAL_ERROR_PATH
    )


def get_error_code(value: Any, fallback: str = "error") -> str:
    code = getattr(value, "code", None)
    return str(code or fallback)


def stringify_error(value: Any) -> str:
    if isinstance(value, ErrorDetail):
        return str(value)

    if isinstance(value, Exception):
        return str(value)

    return str(value)


def build_failure(value: Any, fallback_code: str = "error") -> dict[str, str]:
    return {
        "code": get_error_code(value, fallback_code),
        "message": stringify_error(value),
    }


def build_error_bag(
    *, kind: ErrorKind, failures: list[dict[str, str]]
) -> dict[str, Any]:
    return {
        "kind": kind,
        "failures": failures,
    }


def append_failure(
    errors: dict[str, Any],
    *,
    path: str,
    kind: ErrorKind,
    failure: dict[str, str],
) -> dict[str, Any]:
    if path not in errors:
        errors[path] = build_error_bag(kind=kind, failures=[])

    errors[path]["failures"].append(failure)
    return errors


def append_field_failure(
    errors: dict[str, Any],
    *,
    path: str,
    value: Any,
    fallback_code: str = "invalid",
) -> dict[str, Any]:
    return append_failure(
        errors,
        path=path,
        kind="field",
        failure=build_failure(value, fallback_code),
    )


def append_business_failure(
    errors: dict[str, Any],
    *,
    value: Any,
    path: str = GENERAL_ERROR_PATH,
    fallback_code: str = "error",
) -> dict[str, Any]:
    return append_failure(
        errors,
        path=path,
        kind="business",
        failure=build_failure(value, fallback_code),
    )


def append_system_failure(
    errors: dict[str, Any],
    *,
    value: Any,
    fallback_code: str = "internal_server_error",
) -> dict[str, Any]:
    return append_failure(
        errors,
        path=SYSTEM_ERROR_PATH,
        kind="system",
        failure=build_failure(value, fallback_code),
    )


def normalize_path(path: str) -> str:
    return GENERAL_ERROR_PATH if path == NON_FIELD_ERRORS_KEY else path


def join_path(parent: str, child: str) -> str:
    child = normalize_path(str(child))

    if child in {GENERAL_ERROR_PATH, SYSTEM_ERROR_PATH}:
        return child

    if not parent or parent == GENERAL_ERROR_PATH:
        return child

    return f"{parent}.{child}"


def is_error_bag(value: Any) -> bool:
    return (
        isinstance(value, Mapping)
        and value.get("kind") in {"field", "business", "system"}
        and isinstance(value.get("failures"), list)
    )


def is_error_map(value: Any) -> bool:
    return isinstance(value, Mapping) and all(
        is_error_bag(item) for item in value.values()
    )


def extract_limits(data: Any) -> dict[str, Any] | None:
    if isinstance(data, Mapping) and isinstance(data.get("limits"), Mapping):
        return dict(data["limits"])

    return None


def normalize_errors(
    data: Any,
    *,
    status_code: int | None = None,
    default_code: str | None = None,
) -> dict[str, Any] | None:
    if data in (None, "", [], {}):
        return None

    if isinstance(data, Mapping) and is_error_map(data.get("errors")):
        return dict(data["errors"])

    if is_error_map(data):
        return dict(data)

    fallback_code = default_code or get_default_error_code(status_code)
    errors: dict[str, Any] = {}

    if isinstance(data, Mapping) and "detail" in data:
        detail = data["detail"]
        code = str(data.get("code") or get_error_code(detail, fallback_code))
        kind = get_default_error_kind(status_code)
        path = get_default_error_path(status_code)

        return append_failure(
            errors,
            path=path,
            kind=kind,
            failure=build_failure(detail, code),
        )

    collect_errors(
        errors,
        data,
        path=GENERAL_ERROR_PATH,
        status_code=status_code,
        fallback_code=fallback_code,
    )

    return errors or None


def collect_errors(
    errors: dict[str, Any],
    value: Any,
    *,
    path: str,
    status_code: int | None,
    fallback_code: str,
) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            key = str(key)

            if key in ERROR_METADATA_KEYS:
                continue

            collect_errors(
                errors,
                item,
                path=join_path(path, key),
                status_code=status_code,
                fallback_code=fallback_code,
            )
        return

    if isinstance(value, list | tuple):
        for item in value:
            collect_errors(
                errors,
                item,
                path=path,
                status_code=status_code,
                fallback_code=fallback_code,
            )
        return

    if path in {GENERAL_ERROR_PATH, SYSTEM_ERROR_PATH}:
        kind = get_default_error_kind(status_code)
        append_failure(
            errors,
            path=get_default_error_path(status_code),
            kind=kind,
            failure=build_failure(value, fallback_code),
        )
        return

    append_field_failure(
        errors,
        path=path,
        value=value,
        fallback_code=get_error_code(value, "invalid"),
    )
