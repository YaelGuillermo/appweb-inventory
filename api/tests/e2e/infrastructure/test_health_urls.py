# api/tests/e2e/infrastructure/test_health_urls.py
import pytest
from django.urls import reverse


@pytest.mark.e2e
@pytest.mark.django_db
def test_health_liveness_url_is_available(api_client):
    response = api_client.get(reverse("health:live"))

    assert response.status_code == 200
    assert response.data["status"] == "ok"
    assert response.data["kind"] == "liveness"
