from __future__ import annotations

import pytest
from rest_framework.test import APIClient

from tests.support.accounts.auth.helpers import (
    authorize,
    clear_authorization,
    register_and_login,
)
from tests.support.accounts.auth.paths import AUTH_PATHS
from tests.support.assertions.api_response import (
    expect_error_response,
    expect_success_response,
    expect_user_data,
)


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_get_users_me_returns_current_user(api_client: APIClient) -> None:
    session = register_and_login(api_client)
    authorize(api_client, session["tokens"]["access"])

    response = api_client.get(AUTH_PATHS["me"])

    body = expect_success_response(
        response,
        status_code=200,
        path=AUTH_PATHS["me"],
    )
    expect_user_data(body["data"], email=session["payload"]["email"])


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_get_users_me_without_token_returns_unauthorized(api_client: APIClient) -> None:
    response = api_client.get(AUTH_PATHS["me"])

    expect_error_response(
        response,
        status_code=401,
        path=AUTH_PATHS["me"],
    )


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_get_users_me_with_malformed_token_returns_unauthorized(
    api_client: APIClient,
) -> None:
    authorize(api_client, "malformed-token")

    response = api_client.get(AUTH_PATHS["me"])

    expect_error_response(
        response,
        status_code=401,
        path=AUTH_PATHS["me"],
    )


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_get_users_me_with_refresh_token_returns_unauthorized(
    api_client: APIClient,
) -> None:
    session = register_and_login(api_client)
    authorize(api_client, session["tokens"]["refresh"])

    response = api_client.get(AUTH_PATHS["me"])

    expect_error_response(
        response,
        status_code=401,
        path=AUTH_PATHS["me"],
    )


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_get_users_me_can_clear_credentials(api_client: APIClient) -> None:
    session = register_and_login(api_client)
    authorize(api_client, session["tokens"]["access"])

    authenticated_response = api_client.get(AUTH_PATHS["me"])
    expect_success_response(
        authenticated_response,
        status_code=200,
        path=AUTH_PATHS["me"],
    )

    clear_authorization(api_client)
    response = api_client.get(AUTH_PATHS["me"])

    expect_error_response(
        response,
        status_code=401,
        path=AUTH_PATHS["me"],
    )
