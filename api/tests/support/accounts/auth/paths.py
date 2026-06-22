from __future__ import annotations

API_PREFIX = "/api/v1/accounts"

AUTH_PATHS = {
    "users": f"{API_PREFIX}/users/",
    "me": f"{API_PREFIX}/users/me/",
    "set_password": f"{API_PREFIX}/users/set_password/",
    "jwt_create": f"{API_PREFIX}/jwt/create/",
    "jwt_refresh": f"{API_PREFIX}/jwt/refresh/",
    "jwt_verify": f"{API_PREFIX}/jwt/verify/",
    "social_google": f"{API_PREFIX}/o/google-oauth2/",
}

__all__ = ["API_PREFIX", "AUTH_PATHS"]
