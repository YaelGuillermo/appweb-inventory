# api/config/django/staging.py
from .production import *  # noqa

DEBUG = True  # Staging often needs debug for testing
SECURE_SSL_REDIRECT = False  # Often staging doesn't have SSL
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False