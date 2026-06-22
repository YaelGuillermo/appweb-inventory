# api/config/django/test.py
from __future__ import annotations

from .base import *  # noqa: F403

DEBUG = True
SECRET_KEY = "django-insecure-test-key-only-for-automated-tests"
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CELERY_TASK_ALWAYS_EAGER = True

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "test-cache",
    }
}

REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # noqa: F405
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

SIMPLE_JWT = {
    **SIMPLE_JWT,  # noqa: F405
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

DJOSER = {
    **DJOSER,  # noqa: F405
    # Tests should validate the auth endpoints without depending on SMTP side effects.
    "SEND_CONFIRMATION_EMAIL": False,
    "SEND_ACTIVATION_EMAIL": False,
}
