# api/config/django/base.py
from datetime import timedelta
from pathlib import Path

from django.utils.translation import gettext_lazy as _

from config.env import env

# Build paths
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "core_apps"

# ============================================
# APP IDENTITY & BASE URLS
# ============================================
SITE_NAME = env("SITE_NAME", default="Site")
DOMAIN = env("DOMAIN", default="localhost")
SITE_URL = env("SITE_URL", default="")
API_URL = env("API_URL", default="")
FRONTEND_URL = env("FRONTEND_URL", default="")
API_VERSION = env("API_VERSION", default="v1")
ENVIRONMENT = env("ENVIRONMENT", default="development")

# ============================================
# DJANGO CORE
# ============================================
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")
TIME_ZONE = env("DJANGO_TIME_ZONE", default="UTC")
STATIC_URL = env("DJANGO_STATIC_URL", default="/static/")
MEDIA_URL = env("DJANGO_MEDIA_URL", default="/media/")

# Application definition
DJANGO_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "django_filters",
    "djoser",
    "social_django",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "channels",
    "django_celery_beat",
]

LOCAL_APPS = [
    "database.apps.DatabaseConfig",
    "localization.apps.LocalizationConfig",
    # "core_apps.accounts",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core_apps.common.middleware.request_id.RequestIdMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

# ============================================
# DATABASE - POSTGRESQL
# ============================================
DB_HOST = env("DB_HOST", default="127.0.0.1")
DB_PORT = env.int("DB_PORT", default=5432)
DB_NAME = env("DB_NAME")
DB_USERNAME = env("DB_USERNAME")
DB_PASSWORD = env("DB_PASSWORD")
DB_SCHEMA = env("DB_SCHEMA", default="public")
DB_APPLICATION_SCHEMAS = env.list("DB_APPLICATION_SCHEMAS", default=[DB_SCHEMA])
DB_ADMIN_DATABASE = env("DB_ADMIN_DATABASE", default="postgres")
DB_SSLMODE = env("DB_SSLMODE", default="prefer")
DB_CONNECT_TIMEOUT = env.int("DB_CONNECT_TIMEOUT", default=10)
DB_CONN_MAX_AGE = env.int("DB_CONN_MAX_AGE", default=60)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME,
        "USER": DB_USERNAME,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "CONN_MAX_AGE": DB_CONN_MAX_AGE,
        "OPTIONS": {
            "sslmode": DB_SSLMODE,
            "connect_timeout": DB_CONNECT_TIMEOUT,
        },
    }
}

# Password validation
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ============================================
# INTERNATIONALIZATION
# ============================================
LANGUAGE_CODE = env("DJANGO_LANGUAGE_CODE", default="en-us")
LANGUAGES = [
    ("en-us", _("English")),
    ("es-mx", _("Spanish (Mexico)")),
]
LOCALE_PATHS = [
    BASE_DIR / "locale",
]
I18N_IGNORE_PATTERNS = [
    "venv/*",
    "env/*",
    ".venv/*",
    "staticfiles/*",
    "media/*",
    "logs/*",
    "__pycache__/*",
    "*.pyc",
]

USE_I18N = True
USE_TZ = True
SITE_ID = 1

# Static & Media
STATIC_ROOT = str(BASE_DIR / "staticfiles")
MEDIA_ROOT = str(BASE_DIR / "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
TAGGIT_CASE_INSENSITIVE = True

# ============================================
# SECURITY
# ============================================
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=False)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=False)
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=False)
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=False,
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=False)

# ============================================
# EMAIL
# ============================================
EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="webmaster@localhost")

# ============================================
# DJANGO REST FRAMEWORK
# ============================================
REST_PAGINATION_PAGE_SIZE = env.int("REST_PAGINATION_PAGE_SIZE", default=20)
REST_MAX_PAGE_SIZE = env.int("REST_MAX_PAGE_SIZE", default=100)

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "core_apps.common.renderers.json.CustomJSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": (
        "core_apps.common.pagination.page_number.CustomPageNumberPagination"
    ),
    "PAGE_SIZE": REST_PAGINATION_PAGE_SIZE,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "core_apps.common.exceptions.handler.custom_exception_handler",
}

# ============================================
# JWT
# ============================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env.int("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", default=60)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=env.int("JWT_REFRESH_TOKEN_LIFETIME_DAYS", default=7)
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# ============================================
# DJOSER
# ============================================
DJOSER = {
    "DOMAIN": DOMAIN,
    "SITE_NAME": SITE_NAME,
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "TOKEN_MODEL": None,
}

# ============================================
# AUTH
# ============================================
# AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

# Import sub-configurations
from config.settings.cors import *  # noqa
from config.settings.sessions import *  # noqa
from config.settings.celery import *  # noqa
from config.settings.channels import *  # noqa
from config.settings.auth import *  # noqa
from config.settings.logging import *  # noqa
