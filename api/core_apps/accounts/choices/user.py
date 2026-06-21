# api/core_apps/accounts/choices/user.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    """Application roles assigned to authenticated users."""

    STUDENT = "student", _("Student")
    TEACHER = "teacher", _("Teacher")
    STAFF = "staff", _("Staff")
    ADMIN = "admin", _("Admin")
    DEVELOPER = "developer", _("Developer")
