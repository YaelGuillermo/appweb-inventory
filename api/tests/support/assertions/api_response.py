from __future__ import annotations

import re
from typing import Any
from uuid import UUID

from rest_framework.response import Response

CAMEL_CASE_ENVELOPE_KEYS = {
    "statusCode",
    "detailCode",
    "createdAt",
    "updatedAt",
    "firstName",
    "lastName",
    "isActive",
    "isStaff",
    "dateJoined",
}

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def response_json(response: Response) -> dict[str, Any]:
    body = response.json()
    assert isinstance(body, dict)
    return body


def expect_no_camel_case_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            assert key not in CAMEL_CASE_ENVELOPE_KEYS, (
                f"Unexpected camelCase key: {key}"
            )
            expect_no_camel_case_keys(nested)
        return

    if isinstance(value, list):
        for item in value:
            expect_no_camel_case_keys(item)


def expect_success_response(
    response: Response,
    *,
    status_code: int,
    path: str | None = None,
) -> dict[str, Any]:
    assert response.status_code == status_code
    body = response_json(response)

    assert body["status"] is True
    assert body["status_code"] == status_code
    assert "data" in body
    assert "timestamp" in body

    if path is not None:
        assert body["path"] == path

    expect_no_camel_case_keys(body)
    return body


def expect_error_response(
    response: Response,
    *,
    status_code: int | set[int] | tuple[int, ...] | list[int],
    path: str | None = None,
) -> dict[str, Any]:
    allowed_status_codes = (
        {status_code} if isinstance(status_code, int) else set(status_code)
    )

    assert response.status_code in allowed_status_codes
    body = response_json(response)

    assert body["status"] is False
    assert body["status_code"] == response.status_code
    assert "message" in body
    assert "timestamp" in body

    if path is not None:
        assert body["path"] == path

    expect_no_camel_case_keys(body)
    return body


def expect_uuid(value: Any) -> None:
    assert isinstance(value, str)
    assert UUID(value)
    assert UUID_RE.match(value)


def expect_token_pair(data: dict[str, Any]) -> None:
    assert isinstance(data.get("access"), str)
    assert isinstance(data.get("refresh"), str)
    assert data["access"]
    assert data["refresh"]


def expect_user_data(
    data: dict[str, Any],
    *,
    email: str | None = None,
    role: str | None = None,
) -> None:
    assert isinstance(data, dict)
    expect_uuid(data["id"])
    assert isinstance(data["email"], str)
    assert isinstance(data["first_name"], str)
    assert isinstance(data["last_name"], str)
    assert isinstance(data["role"], str)

    if email is not None:
        assert data["email"] == email.lower()

    if role is not None:
        assert data["role"] == role

    expect_no_camel_case_keys(data)


def expect_error_field(body: dict[str, Any], field_name: str) -> None:
    errors = body.get("errors")
    assert errors is not None

    if isinstance(errors, dict):
        assert field_name in errors or any(
            str(key).endswith(f".{field_name}") for key in errors
        )
        return

    if isinstance(errors, list):
        serialized = str(errors)
        assert field_name in serialized
        return

    assert field_name in str(errors)


__all__ = [
    "expect_error_field",
    "expect_error_response",
    "expect_no_camel_case_keys",
    "expect_success_response",
    "expect_token_pair",
    "expect_user_data",
    "expect_uuid",
    "response_json",
]
