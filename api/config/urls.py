# api/config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("health/", include("core_apps.infrastructure.health.urls")),
    path(
        "api/v1/",
        include(
            [
                path("accounts/", include("core_apps.accounts.urls.main_urls")),
                path("infra/", include("core_apps.infrastructure.urls")),
            ]
        ),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
