# api/config/settings/infrastructure.py
from pathlib import Path

from config.env import env

_BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ============================================
# INFRASTRUCTURE HEALTH CHECKS
# ============================================
HEALTH_CHECKS_ENABLED = env.bool("HEALTH_CHECKS_ENABLED", default=True)
HEALTH_CHECK_DETAILS_ENABLED = env.bool(
    "HEALTH_CHECK_DETAILS_ENABLED",
    default=False,
)

# ============================================
# HTTP REQUEST LOGGING
# ============================================
HTTP_REQUEST_LOGGING_ENABLED = env.bool(
    "HTTP_REQUEST_LOGGING_ENABLED",
    default=True,
)

# ============================================
# MEDIA STORAGE
# ============================================
USE_AWS_STORAGE = env.bool("USE_AWS_STORAGE", default=False)
MEDIA_STORAGE_PUBLIC_URL = env("MEDIA_STORAGE_PUBLIC_URL", default="")
MEDIA_STORAGE_LOCAL_ROOT = env(
    "MEDIA_STORAGE_LOCAL_ROOT",
    default=str(_BASE_DIR / "media"),
)
MEDIA_FILE_MAX_SIZE_BYTES = env.int(
    "MEDIA_FILE_MAX_SIZE_BYTES", default=5 * 1024 * 1024
)
MEDIA_IMAGE_ALLOWED_MIME_TYPES = env.list(
    "MEDIA_IMAGE_ALLOWED_MIME_TYPES",
    default=["image/jpeg", "image/png", "image/webp"],
)

if USE_AWS_STORAGE:
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="")
    AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN", default="")
    AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL", default=None)
    AWS_QUERYSTRING_AUTH = env.bool("AWS_QUERYSTRING_AUTH", default=False)
    AWS_S3_FILE_OVERWRITE = env.bool("AWS_S3_FILE_OVERWRITE", default=False)

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": MEDIA_STORAGE_LOCAL_ROOT,
                "base_url": "/media/",
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# ============================================
# SQL ASSETS
# ============================================
SQL_ASSETS_MANIFEST_MODULE = env(
    "SQL_ASSETS_MANIFEST_MODULE",
    default="core_apps.infrastructure.sql_assets.manifest",
)
