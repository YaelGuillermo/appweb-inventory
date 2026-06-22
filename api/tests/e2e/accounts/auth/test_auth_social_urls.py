from __future__ import annotations

import pytest
from django.urls import resolve
from rest_framework.test import APIClient

from tests.support.accounts.auth.paths import AUTH_PATHS
from tests.support.assertions.api_response import expect_error_response


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
def test_google_social_auth_url_is_registered() -> None:
    match = resolve(AUTH_PATHS["social_google"])
    assert match.func is not None


@pytest.mark.e2e
@pytest.mark.accounts
@pytest.mark.auth
@pytest.mark.django_db
def test_google_social_auth_rejects_empty_payload(api_client: APIClient) -> None:
    response = api_client.post(AUTH_PATHS["social_google"], {}, format="json")

    expect_error_response(
        response,
        status_code={400, 401},
        path=AUTH_PATHS["social_google"],
    )
