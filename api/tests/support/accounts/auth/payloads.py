from __future__ import annotations

from uuid import uuid4

DEFAULT_TEST_PASSWORD = "Strongp@ssword1!"
DEFAULT_NEW_TEST_PASSWORD = "NewStrongp@ssword2!"


def unique_email(prefix: str = "test_user") -> str:
    suffix = uuid4().hex[:12]
    return f"{prefix}_{suffix}@example.com"


def make_register_payload(**overrides):
    email = overrides.pop("email", unique_email())
    password = overrides.pop("password", DEFAULT_TEST_PASSWORD)

    payload = {
        "email": email,
        "first_name": "Test",
        "last_name": "User",
        "password": password,
        "re_password": password,
    }
    payload.update(overrides)
    return payload


def make_login_payload(
    email: str, password: str = DEFAULT_TEST_PASSWORD
) -> dict[str, str]:
    return {
        "email": email,
        "password": password,
    }


def make_refresh_payload(refresh_token: str) -> dict[str, str]:
    return {"refresh": refresh_token}


def make_verify_payload(token: str) -> dict[str, str]:
    return {"token": token}


__all__ = [
    "DEFAULT_NEW_TEST_PASSWORD",
    "DEFAULT_TEST_PASSWORD",
    "make_login_payload",
    "make_refresh_payload",
    "make_register_payload",
    "make_verify_payload",
    "unique_email",
]
