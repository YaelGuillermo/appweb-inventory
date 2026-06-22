from __future__ import annotations

from typing import Any

from rest_framework.response import Response
from rest_framework.test import APIClient

from tests.support.accounts.auth.paths import AUTH_PATHS
from tests.support.accounts.auth.payloads import (
    DEFAULT_TEST_PASSWORD,
    make_login_payload,
    make_register_payload,
)
from tests.support.assertions.api_response import (
    expect_success_response,
    expect_token_pair,
)


def register_user(
    api_client: APIClient,
    payload: dict[str, Any] | None = None,
) -> tuple[Response, dict[str, Any], dict[str, Any]]:
    register_payload = payload or make_register_payload()
    response = api_client.post(AUTH_PATHS["users"], register_payload, format="json")
    body = expect_success_response(
        response,
        status_code=201,
        path=AUTH_PATHS["users"],
    )
    return response, body, register_payload


def login_user(
    api_client: APIClient,
    *,
    email: str,
    password: str = DEFAULT_TEST_PASSWORD,
) -> tuple[Response, dict[str, Any]]:
    response = api_client.post(
        AUTH_PATHS["jwt_create"],
        make_login_payload(email, password),
        format="json",
    )
    body = expect_success_response(
        response,
        status_code=200,
        path=AUTH_PATHS["jwt_create"],
    )
    expect_token_pair(body["data"])
    return response, body


def register_and_login(api_client: APIClient) -> dict[str, Any]:
    _, _, payload = register_user(api_client)
    _, login_body = login_user(
        api_client,
        email=payload["email"],
        password=payload["password"],
    )

    return {
        "payload": payload,
        "tokens": login_body["data"],
    }


def authorize(api_client: APIClient, access_token: str) -> None:
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")


def clear_authorization(api_client: APIClient) -> None:
    api_client.credentials()


__all__ = [
    "authorize",
    "clear_authorization",
    "login_user",
    "register_and_login",
    "register_user",
]
