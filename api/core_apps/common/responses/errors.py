from __future__ import annotations

from typing import Any

from rest_framework.exceptions import ErrorDetail

GENERAL_ERROR_PATH = "general"
SYSTEM_ERROR_PATH = "system"


def get_error_code(value: Any, fallback: str = "error") -> str:
    code = getattr(value, "code", None)
    return str(code or fallback)


def stringify_error(value: Any) -> str:
    if isinstance(value, ErrorDetail):
        return str(value)

    if isinstance(value, str):
        return value

    return str(value)


def build_failure(value: Any, fallback_code: str = "error") -> dict[str, str]:
    return {
        "code": get_error_code(value, fallback_code),
        "message": stringify_error(value),
    }


def build_error_bag(
    *,
    kind: str,
    failures: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "kind": kind,
        "failures": failures,
    }


def normalize_errors(data: Any) -> dict[str, Any] | None:
    if data in (None, "", [], {}):
        return None

    if isinstance(data, dict) and isinstance(data.get("errors"), dict):
        return data["errors"]

    if isinstance(data, dict) and "detail" in data:
        return {
            GENERAL_ERROR_PATH: build_error_bag(
                kind="business",
                failures=[build_failure(data["detail"])],
            )
        }

    if isinstance(data, dict):
        errors: dict[str, Any] = {}

        for field, value in data.items():
            values = value if isinstance(value, list) else [value]
            errors[str(field)] = build_error_bag(
                kind="field",
                failures=[build_failure(item, "invalid") for item in values],
            )

        return errors or None

    values = data if isinstance(data, list) else [data]
    return {
        GENERAL_ERROR_PATH: build_error_bag(
            kind="business",
            failures=[build_failure(item) for item in values],
        )
    }
