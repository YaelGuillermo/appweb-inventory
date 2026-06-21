# api/core_apps/accounts/serializers/auth.py
from __future__ import annotations

from typing import Any

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core_apps.accounts.models import User
from core_apps.accounts.serializers.users import CurrentUserSerializer


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT serializer that normalizes email and returns a snake_case user block."""

    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        username_field = self.username_field
        raw_email = attrs.get(username_field)

        if raw_email:
            attrs[username_field] = User.objects.normalize_email(str(raw_email))

        data = super().validate(attrs)
        data["user"] = CurrentUserSerializer(
            self.user,
            context=self.context,
        ).data
        return data
