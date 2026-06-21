# api/core_apps/accounts/managers/user.py
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from core_apps.accounts.choices import UserRole

if TYPE_CHECKING:
    from core_apps.accounts.models.user import User


class UserQuerySet(models.QuerySet):
    """Chainable queryset helpers for the custom user model."""

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def staff(self):
        return self.filter(is_staff=True)

    def superusers(self):
        return self.filter(is_superuser=True)

    def students(self):
        return self.filter(role=UserRole.STUDENT)

    def teachers(self):
        return self.filter(role=UserRole.TEACHER)

    def developers(self):
        return self.filter(role=UserRole.DEVELOPER)

    def by_email(self, email: str):
        return self.filter(email=UserManager.normalize_email_value(email))


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    """Manager for an email-based custom user model."""

    use_in_migrations = True

    @staticmethod
    def normalize_email_value(email: str | None) -> str:
        normalized = BaseUserManager.normalize_email(str(email or "").strip())
        return normalized.lower()

    def normalize_email(self, email: str | None) -> str:
        return self.normalize_email_value(email)

    def _create_user(
        self,
        email: str,
        password: str | None,
        **extra_fields: Any,
    ) -> User:
        email = self.normalize_email(email)
        if not email:
            raise ValueError("The email address is required.")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean(exclude=["password"])
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> User:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", UserRole.STUDENT)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRole.DEVELOPER)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
