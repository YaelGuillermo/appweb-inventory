from __future__ import annotations

import pytest
from rest_framework.test import APIClient

from tests.support.accounts.auth.paths import AUTH_PATHS
from tests.support.accounts.auth.payloads import (
    DEFAULT_TEST_PASSWORD,
    make_register_payload,
)
from tests.support.assertions.api_response import (
    expect_error_field,
    expect_error_response,
    expect_success_response,
    expect_user_data,
)


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_users_registers_a_user(api_client: APIClient) -> None:
    payload = make_register_payload()

    response = api_client.post(AUTH_PATHS["users"], payload, format="json")

    body = expect_success_response(
        response,
        status_code=201,
        path=AUTH_PATHS["users"],
    )
    expect_user_data(body["data"], email=payload["email"])


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_users_rejects_duplicate_email(api_client: APIClient) -> None:
    payload = make_register_payload()
    first_response = api_client.post(AUTH_PATHS["users"], payload, format="json")
    expect_success_response(first_response, status_code=201, path=AUTH_PATHS["users"])

    duplicate_payload = make_register_payload(email=payload["email"])
    response = api_client.post(AUTH_PATHS["users"], duplicate_payload, format="json")

    body = expect_error_response(
        response,
        status_code={400, 409},
        path=AUTH_PATHS["users"],
    )
    expect_error_field(body, "email")


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_users_rejects_empty_payload(api_client: APIClient) -> None:
    response = api_client.post(AUTH_PATHS["users"], {}, format="json")

    body = expect_error_response(
        response,
        status_code=400,
        path=AUTH_PATHS["users"],
    )
    expect_error_field(body, "email")
    expect_error_field(body, "password")


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_users_rejects_invalid_email(api_client: APIClient) -> None:
    response = api_client.post(
        AUTH_PATHS["users"],
        make_register_payload(email="not-an-email"),
        format="json",
    )

    body = expect_error_response(
        response,
        status_code=400,
        path=AUTH_PATHS["users"],
    )
    expect_error_field(body, "email")


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_users_rejects_weak_password(api_client: APIClient) -> None:
    response = api_client.post(
        AUTH_PATHS["users"],
        make_register_payload(password="short"),
        format="json",
    )

    body = expect_error_response(
        response,
        status_code=400,
        path=AUTH_PATHS["users"],
    )
    expect_error_field(body, "password")


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_users_rejects_password_confirmation_mismatch(
    api_client: APIClient,
) -> None:
    payload = make_register_payload(password=DEFAULT_TEST_PASSWORD)
    payload["re_password"] = "Differentp@ssword2!"

    response = api_client.post(AUTH_PATHS["users"], payload, format="json")

    body = expect_error_response(
        response,
        status_code=400,
        path=AUTH_PATHS["users"],
    )
    expect_error_field(body, "non_field_errors")
