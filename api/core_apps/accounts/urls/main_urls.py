# api/core_apps/accounts/urls/main_urls.py
from django.urls import include, path

app_name = "accounts"

urlpatterns = [
    path("", include("core_apps.accounts.urls.auth_urls")),
]
