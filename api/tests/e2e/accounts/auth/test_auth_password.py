from __future__ import annotations

import pytest
from rest_framework.test import APIClient

from tests.support.accounts.auth.helpers import (
    authorize,
    login_user,
    register_and_login,
)
from tests.support.accounts.auth.paths import AUTH_PATHS
from tests.support.accounts.auth.payloads import DEFAULT_NEW_TEST_PASSWORD
from tests.support.assertions.api_response import (
    expect_error_field,
    expect_error_response,
)


def make_set_password_payload(
    *,
    current_password: str,
    new_password: str = DEFAULT_NEW_TEST_PASSWORD,
    re_new_password: str = DEFAULT_NEW_TEST_PASSWORD,
) -> dict[str, str]:
    return {
        "current_password": current_password,
        "new_password": new_password,
        "re_new_password": re_new_password,
    }


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_set_password_updates_current_user_password(api_client: APIClient) -> None:
    session = register_and_login(api_client)
    authorize(api_client, session["tokens"]["access"])

    response = api_client.post(
        AUTH_PATHS["set_password"],
        make_set_password_payload(current_password=session["payload"]["password"]),
        format="json",
    )

    assert response.status_code == 204

    _, login_body = login_user(
        api_client,
        email=session["payload"]["email"],
        password=DEFAULT_NEW_TEST_PASSWORD,
    )
    assert isinstance(login_body["data"]["access"], str)


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_set_password_without_token_returns_unauthorized(
    api_client: APIClient,
) -> None:
    response = api_client.post(
        AUTH_PATHS["set_password"],
        make_set_password_payload(current_password="Strongp@ssword1!"),
        format="json",
    )

    expect_error_response(
        response,
        status_code=401,
        path=AUTH_PATHS["set_password"],
    )


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_set_password_rejects_wrong_current_password(
    api_client: APIClient,
) -> None:
    session = register_and_login(api_client)
    authorize(api_client, session["tokens"]["access"])

    response = api_client.post(
        AUTH_PATHS["set_password"],
        make_set_password_payload(current_password="Wrongp@ssword1!"),
        format="json",
    )

    body = expect_error_response(
        response,
        status_code=400,
        path=AUTH_PATHS["set_password"],
    )
    expect_error_field(body, "current_password")


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_post_set_password_rejects_mismatched_confirmation(
    api_client: APIClient,
) -> None:
    session = register_and_login(api_client)
    authorize(api_client, session["tokens"]["access"])

    response = api_client.post(
        AUTH_PATHS["set_password"],
        make_set_password_payload(
            current_password=session["payload"]["password"],
            re_new_password="Differentp@ssword3!",
        ),
        format="json",
    )

    body = expect_error_response(
        response,
        status_code=400,
        path=AUTH_PATHS["set_password"],
    )
    expect_error_field(body, "non_field_errors")
