# api/core_apps/infrastructure/health/urls.py
from django.urls import path

from core_apps.infrastructure.health.views import (
    HealthView,
    LivenessHealthView,
    ReadinessHealthView,
)

app_name = "health"

urlpatterns = [
    path("", HealthView.as_view(), name="full"),
    path("live/", LivenessHealthView.as_view(), name="live"),
    path("ready/", ReadinessHealthView.as_view(), name="ready"),
]
