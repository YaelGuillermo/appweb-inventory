# api/config/settings/sessions.py
from config.env import env

SESSION_COOKIE_AGE = env.int("DJANGO_SESSION_COOKIE_AGE", default=1209600)  # 2 weeks
SESSION_COOKIE_NAME = env("DJANGO_SESSION_COOKIE_NAME", default="sessionid")
SESSION_SAVE_EVERY_REQUEST = env.bool(
    "DJANGO_SESSION_SAVE_EVERY_REQUEST", default=False
)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
