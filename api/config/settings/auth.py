# api/config/settings/auth.py
from config.env import env

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", default="")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", default="")
SOCIAL_AUTH_ALLOWED_REDIRECT_URIS = env.list(
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS", default=[]
)
GOOGLE_HD = env("GOOGLE_HD", default="")
GOOGLE_PROMPT = env("GOOGLE_PROMPT", default="select_account")

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
