# api/core_apps/accounts/models/user.py
from __future__ import annotations

import uuid
from typing import Any

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core_apps.accounts.choices import UserRole
from core_apps.accounts.constants import (
    USER_EMAIL_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_ROLE_MAX_LENGTH,
)
from core_apps.accounts.managers import UserManager
from core_apps.common.normalizers import normalize_human_name
from core_apps.common.validators import validate_name_rules


class User(AbstractBaseUser, PermissionsMixin):
    """
    Email-based user model for API authentication.

    This model intentionally does not inherit from common BaseModel because
    Django authentication needs AbstractBaseUser and PermissionsMixin as the
    source of truth for credentials and permissions.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID"),
    )
    email = models.EmailField(
        max_length=USER_EMAIL_MAX_LENGTH,
        unique=True,
        db_index=True,
        verbose_name=_("Email"),
        error_messages={
            "unique": _("A user with this email already exists."),
        },
    )
    first_name = models.CharField(
        max_length=USER_NAME_MAX_LENGTH,
        verbose_name=_("First name"),
        validators=[validate_name_rules],
    )
    last_name = models.CharField(
        max_length=USER_NAME_MAX_LENGTH,
        verbose_name=_("Last name"),
        validators=[validate_name_rules],
    )
    role = models.CharField(
        max_length=USER_ROLE_MAX_LENGTH,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        db_index=True,
        verbose_name=_("Role"),
        help_text=_("Application role assigned to this user."),
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name=_("Active"),
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Staff status"),
        help_text=_("Designates whether the user can log into the admin site."),
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        verbose_name=_("Date joined"),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ["email"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [
            models.Index(
                fields=["role", "is_active"],
                name="accounts_user_role_active_idx",
            ),
            models.Index(
                fields=["date_joined"],
                name="accounts_user_joined_idx",
            ),
        ]

    @property
    def full_name(self) -> str:
        return self.get_full_name()

    @property
    def short_name(self) -> str:
        return self.get_short_name()

    def clean(self) -> None:
        super().clean()
        self.email = User.objects.normalize_email(self.email)
        self.first_name = normalize_human_name(self.first_name)
        self.last_name = normalize_human_name(self.last_name)

    def get_full_name(self) -> str:
        return normalize_human_name(f"{self.first_name} {self.last_name}")

    def get_short_name(self) -> str:
        return self.first_name

    def natural_key(self) -> tuple[str]:
        return (self.email,)

    def email_user(
        self,
        subject: str,
        message: str,
        from_email: str | None = None,
        **kwargs: Any,
    ) -> None:
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def soft_delete(self, *, save: bool = True) -> None:
        self.is_active = False
        if save:
            self.save(update_fields=["is_active"])

    def restore(self, *, save: bool = True) -> None:
        self.is_active = True
        if save:
            self.save(update_fields=["is_active"])

    def hard_delete(self, using: str | None = None, keep_parents: bool = False):
        return super().delete(using=using, keep_parents=keep_parents)

    def delete(
        self,
        using: str | None = None,
        keep_parents: bool = False,
        *,
        hard: bool = False,
    ):
        if hard:
            return self.hard_delete(using=using, keep_parents=keep_parents)

        self.soft_delete()
        return 1, {self._meta.label: 1}

    def __str__(self) -> str:
        return self.email
