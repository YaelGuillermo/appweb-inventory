# api/core_apps/accounts/urls/auth_urls.py
from django.urls import include, path

urlpatterns = [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
    path("", include("djoser.social.urls")),
]
