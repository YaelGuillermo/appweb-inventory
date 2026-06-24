# api/core_apps/infrastructure/urls.py
from django.urls import include, path

app_name = "infrastructure"

urlpatterns = [
    path("health/", include("core_apps.infrastructure.health.urls")),
]
