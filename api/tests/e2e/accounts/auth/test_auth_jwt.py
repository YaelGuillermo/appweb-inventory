from __future__ import annotations

import pytest
from rest_framework.test import APIClient

from tests.factories.accounts.user_factory import UserFactory
from tests.support.accounts.auth.helpers import (
    login_user,
    register_and_login,
    register_user,
)
from tests.support.accounts.auth.paths import AUTH_PATHS
from tests.support.accounts.auth.payloads import (
    DEFAULT_TEST_PASSWORD,
    make_login_payload,
    make_refresh_payload,
    make_verify_payload,
)
from tests.support.assertions.api_response import (
    expect_error_field,
    expect_error_response,
    expect_success_response,
    expect_token_pair,
    expect_user_data,
)
from tests.support.assertions.jwt import expect_valid_jwt


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_jwt_create_returns_access_and_refresh_tokens(
    api_client: APIClient,
) -> None:
    _, _, payload = register_user(api_client)

    response, body = login_user(
        api_client,
        email=payload["email"],
        password=payload["password"],
    )

    assert response.status_code == 200
    expect_token_pair(body["data"])
    expect_valid_jwt(body["data"]["access"])
    expect_valid_jwt(body["data"]["refresh"])

    if "user" in body["data"]:
        expect_user_data(body["data"]["user"], email=payload["email"])


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_jwt_create_rejects_wrong_password(api_client: APIClient) -> None:
    _, _, payload = register_user(api_client)

    response = api_client.post(
        AUTH_PATHS["jwt_create"],
        make_login_payload(payload["email"], "Wrongp@ssword1!"),
        format="json",
    )

    expect_error_response(
        response,
        status_code=401,
        path=AUTH_PATHS["jwt_create"],
    )


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_jwt_create_rejects_unknown_email(api_client: APIClient) -> None:
    response = api_client.post(
        AUTH_PATHS["jwt_create"],
        make_login_payload("unknown@example.com"),
        format="json",
    )

    expect_error_response(
        response,
        status_code=401,
        path=AUTH_PATHS["jwt_create"],
    )


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_jwt_create_rejects_inactive_user(api_client: APIClient) -> None:
    user = UserFactory(is_active=False, password=DEFAULT_TEST_PASSWORD)

    response = api_client.post(
        AUTH_PATHS["jwt_create"],
        make_login_payload(user.email, DEFAULT_TEST_PASSWORD),
        format="json",
    )

    expect_error_response(
        response,
        status_code=401,
        path=AUTH_PATHS["jwt_create"],
    )


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_jwt_create_rejects_empty_payload(api_client: APIClient) -> None:
    response = api_client.post(AUTH_PATHS["jwt_create"], {}, format="json")

    body = expect_error_response(
        response,
        status_code=400,
        path=AUTH_PATHS["jwt_create"],
    )
    expect_error_field(body, "email")
    expect_error_field(body, "password")


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_jwt_refresh_returns_new_access_token(api_client: APIClient) -> None:
    session = register_and_login(api_client)

    response = api_client.post(
        AUTH_PATHS["jwt_refresh"],
        make_refresh_payload(session["tokens"]["refresh"]),
        format="json",
    )

    body = expect_success_response(
        response,
        status_code=200,
        path=AUTH_PATHS["jwt_refresh"],
    )
    assert isinstance(body["data"].get("access"), str)
    expect_valid_jwt(body["data"]["access"])

    if "refresh" in body["data"]:
        expect_valid_jwt(body["data"]["refresh"])


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_jwt_refresh_rejects_empty_payload(api_client: APIClient) -> None:
    response = api_client.post(AUTH_PATHS["jwt_refresh"], {}, format="json")

    body = expect_error_response(
        response,
        status_code=400,
        path=AUTH_PATHS["jwt_refresh"],
    )
    expect_error_field(body, "refresh")


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_jwt_refresh_rejects_malformed_token(api_client: APIClient) -> None:
    response = api_client.post(
        AUTH_PATHS["jwt_refresh"],
        make_refresh_payload("malformed-token"),
        format="json",
    )

    expect_error_response(
        response,
        status_code={400, 401},
        path=AUTH_PATHS["jwt_refresh"],
    )


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_jwt_verify_accepts_valid_access_token(api_client: APIClient) -> None:
    session = register_and_login(api_client)

    response = api_client.post(
        AUTH_PATHS["jwt_verify"],
        make_verify_payload(session["tokens"]["access"]),
        format="json",
    )

    expect_success_response(
        response,
        status_code=200,
        path=AUTH_PATHS["jwt_verify"],
    )


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_jwt_verify_rejects_malformed_token(api_client: APIClient) -> None:
    response = api_client.post(
        AUTH_PATHS["jwt_verify"],
        make_verify_payload("malformed-token"),
        format="json",
    )

    expect_error_response(
        response,
        status_code={400, 401},
        path=AUTH_PATHS["jwt_verify"],
    )
