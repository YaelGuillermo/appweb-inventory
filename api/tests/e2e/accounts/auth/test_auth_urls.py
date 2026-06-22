from __future__ import annotations

import pytest
from django.urls import resolve
from rest_framework.test import APIClient

from tests.support.accounts.auth.paths import AUTH_PATHS


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
def test_djoser_auth_urls_are_registered(api_client: APIClient) -> None:
    for path_name in (
        "users",
        "me",
        "jwt_create",
        "jwt_refresh",
        "jwt_verify",
        "social_google",
    ):
        match = resolve(AUTH_PATHS[path_name])
        assert match.func is not None


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
def test_auth_urls_accept_options_requests(api_client: APIClient) -> None:
    for path_name in ("users", "jwt_create", "jwt_refresh", "jwt_verify"):
        response = api_client.options(AUTH_PATHS[path_name])
        assert response.status_code in {200, 401, 403, 405}
