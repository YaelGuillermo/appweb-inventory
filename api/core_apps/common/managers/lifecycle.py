# api/core_apps/common/managers/lifecycle.py
from django.db import models

from core_apps.common.querysets import LifecycleQuerySet


class LifecycleManager(models.Manager.from_queryset(LifecycleQuerySet)):
    """
    Single manager for lifecycle-aware models.

    It intentionally does not hide records automatically. Each view/service must
    choose the right queryset method: `.active()`, `.trashed()`, `.removed()`,
    `.visible_to_user()`, `.visible_in_trash()`, or `.visible_to_admin()`.
    """

    pass
