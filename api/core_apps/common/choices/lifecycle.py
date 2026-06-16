# api/core_apps/common/choices/lifecycle.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class LifecycleState(models.TextChoices):
    """
    User-facing lifecycle state for records that should remain in the database.

    ACTIVE:
        Visible in the normal user experience.
    TRASHED:
        First delete. Visible only in the user's trash/recycle bin.
    REMOVED:
        Second delete. Hidden from normal user areas and trash, but still stored
        for admin, audit, retention, and recovery workflows.
    """

    ACTIVE = "active", _("Active")
    TRASHED = "trashed", _("Trashed")
    REMOVED = "removed", _("Removed")


class LifecycleStrategy(models.TextChoices):
    """
    Strategy used when a lifecycle transition may affect related children.

    SHALLOW:
        Transition only the current object/queryset.
    DEEP:
        Transition the current object/queryset and child querysets explicitly
        returned by `get_lifecycle_children()`.
    """

    SHALLOW = "shallow", _("Shallow")
    DEEP = "deep", _("Deep")
