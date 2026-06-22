from __future__ import annotations

from rest_framework_simplejwt.tokens import UntypedToken


def expect_valid_jwt(token: str) -> None:
    assert isinstance(token, str)
    assert token
    UntypedToken(token)


__all__ = ["expect_valid_jwt"]
