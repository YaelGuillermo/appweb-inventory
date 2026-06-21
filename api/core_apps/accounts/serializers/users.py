# api/core_apps/accounts/serializers/users.py
from __future__ import annotations

from djoser.serializers import (
    UserCreatePasswordRetypeSerializer,
    UserSerializer as DjoserUserSerializer,
)
from rest_framework import serializers

from core_apps.accounts.models import User


class UserBaseSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
        )
        read_only_fields = ("id", "full_name", "role")


class UserListSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + (
            "is_active",
            "is_staff",
            "date_joined",
        )
        read_only_fields = UserBaseSerializer.Meta.read_only_fields + (
            "is_active",
            "is_staff",
            "date_joined",
        )


class UserDetailSerializer(UserListSerializer):
    class Meta(UserListSerializer.Meta):
        fields = UserListSerializer.Meta.fields + ("last_login",)
        read_only_fields = UserListSerializer.Meta.read_only_fields + ("last_login",)


class UserSerializer(DjoserUserSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "is_active",
            "is_staff",
            "date_joined",
            "last_login",
        )
        read_only_fields = fields


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields
        read_only_fields = UserSerializer.Meta.read_only_fields


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "password",
            "re_password",
        )
        read_only_fields = ("id", "full_name", "role")
        extra_kwargs = {
            "password": {"write_only": True},
            "re_password": {"write_only": True},
        }

    def validate_email(self, value: str) -> str:
        email = User.objects.normalize_email(value)
        queryset = User.objects.filter(email__iexact=email)

        if queryset.exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return email
