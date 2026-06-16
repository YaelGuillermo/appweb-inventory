# api/core_apps/common/models/base.py
from __future__ import annotations

import uuid
from collections.abc import Iterable

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core_apps.common.choices import LifecycleState, LifecycleStrategy
from core_apps.common.constants import LIFECYCLE_STATE_MAX_LENGTH
from core_apps.common.managers import LifecycleManager
from core_apps.common.services import cascade_lifecycle_transition, delete_result


class BaseModel(models.Model):
    """
    Abstract base model with UUID identity, timestamps, audit fields, and a
    two-step logical lifecycle.

    Lifecycle flow:
        active -> trashed -> removed

    Removed records stay in the database for admin, audit, retention, and
    recovery workflows, but are hidden from normal users and trash views.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
        verbose_name=_("Created by"),
        help_text=_("User who created this record."),
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated",
        verbose_name=_("Updated by"),
        help_text=_("User who last updated this record."),
    )
    lifecycle_state = models.CharField(
        max_length=LIFECYCLE_STATE_MAX_LENGTH,
        choices=LifecycleState.choices,
        default=LifecycleState.ACTIVE,
        db_index=True,
        verbose_name=_("Lifecycle state"),
        help_text=_("Current lifecycle state for user-facing visibility."),
    )
    trashed_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        db_index=True,
        verbose_name=_("Trashed at"),
        help_text=_("When this record entered the user's trash."),
    )
    trashed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_trashed",
        verbose_name=_("Trashed by"),
        help_text=_("User who moved this record to trash."),
    )
    removed_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        db_index=True,
        verbose_name=_("Removed at"),
        help_text=_("When this record was removed from the user's trash."),
    )
    removed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_removed",
        verbose_name=_("Removed by"),
        help_text=_("User who performed the second deletion."),
    )

    objects = LifecycleManager()

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        get_latest_by = "created_at"
        indexes = [
            models.Index(
                fields=["lifecycle_state", "created_at"],
                name="%(app_label)s_%(class)s_state_created_idx",
            ),
            models.Index(
                fields=["trashed_at"],
                name="%(app_label)s_%(class)s_trashed_at_idx",
            ),
            models.Index(
                fields=["removed_at"],
                name="%(app_label)s_%(class)s_removed_at_idx",
            ),
        ]

    @property
    def is_active(self) -> bool:
        return self.lifecycle_state == LifecycleState.ACTIVE

    @property
    def is_trashed(self) -> bool:
        return self.lifecycle_state == LifecycleState.TRASHED

    @property
    def is_removed(self) -> bool:
        return self.lifecycle_state == LifecycleState.REMOVED

    @property
    def is_visible_to_user(self) -> bool:
        return self.is_active

    @property
    def is_visible_in_trash(self) -> bool:
        return self.is_trashed

    def get_lifecycle_children(self) -> Iterable[models.QuerySet]:
        """
        Return child querysets that should follow deep lifecycle transitions.

        Override this in concrete parent models when cascading is part of the
        domain rule. The default is intentionally empty.
        """
        return ()

    def trash(
        self,
        *,
        actor=None,
        strategy: str | LifecycleStrategy = LifecycleStrategy.SHALLOW,
        save: bool = True,
    ) -> bool:
        """First deletion: move this active record to the user's trash."""
        if not self.is_active:
            return False

        now = timezone.now()
        self.lifecycle_state = LifecycleState.TRASHED
        self.trashed_at = now
        self.removed_at = None
        self.removed_by = None
        self.updated_at = now

        update_fields = [
            "lifecycle_state",
            "trashed_at",
            "removed_at",
            "removed_by",
            "updated_at",
        ]

        if actor is not None:
            self.trashed_by = actor
            self.updated_by = actor
            update_fields.extend(["trashed_by", "updated_by"])

        if save:
            self.save(update_fields=update_fields)

        cascade_lifecycle_transition(
            self,
            action="trash",
            actor=actor,
            strategy=strategy,
        )
        return True

    def remove(
        self,
        *,
        actor=None,
        strategy: str | LifecycleStrategy = LifecycleStrategy.SHALLOW,
        save: bool = True,
    ) -> bool:
        """Second deletion: hide this trashed record from user-facing flows."""
        if not self.is_trashed:
            return False

        now = timezone.now()
        self.lifecycle_state = LifecycleState.REMOVED
        self.removed_at = now
        self.updated_at = now

        update_fields = ["lifecycle_state", "removed_at", "updated_at"]

        if actor is not None:
            self.removed_by = actor
            self.updated_by = actor
            update_fields.extend(["removed_by", "updated_by"])

        if save:
            self.save(update_fields=update_fields)

        cascade_lifecycle_transition(
            self,
            action="remove",
            actor=actor,
            strategy=strategy,
        )
        return True

    def restore(
        self,
        *,
        actor=None,
        include_removed: bool = False,
        strategy: str | LifecycleStrategy = LifecycleStrategy.SHALLOW,
        save: bool = True,
    ) -> bool:
        """
        Restore this record to active.

        Removed records require `include_removed=True`, making admin/system
        recovery explicit.
        """
        if self.is_active or (self.is_removed and not include_removed):
            return False

        self.lifecycle_state = LifecycleState.ACTIVE
        self.trashed_at = None
        self.trashed_by = None
        self.removed_at = None
        self.removed_by = None
        self.updated_at = timezone.now()

        update_fields = [
            "lifecycle_state",
            "trashed_at",
            "trashed_by",
            "removed_at",
            "removed_by",
            "updated_at",
        ]

        if actor is not None:
            self.updated_by = actor
            update_fields.append("updated_by")

        if save:
            self.save(update_fields=update_fields)

        cascade_lifecycle_transition(
            self,
            action="restore",
            actor=actor,
            strategy=strategy,
            include_removed=include_removed,
        )
        return True

    def hard_delete(self, using=None, keep_parents: bool = False):
        """Physically delete this record. Reserve for exceptional maintenance."""
        return super().delete(using=using, keep_parents=keep_parents)

    def delete(
        self,
        using=None,
        keep_parents: bool = False,
        *,
        actor=None,
        strategy: str | LifecycleStrategy = LifecycleStrategy.SHALLOW,
        hard: bool = False,
    ):
        """
        Advance this record one lifecycle level.

        First call: active -> trashed.
        Second call: trashed -> removed.
        Removed records stay in the database unless `hard=True` is explicit.
        """
        if hard:
            return self.hard_delete(using=using, keep_parents=keep_parents)

        changed = False

        if self.is_active:
            changed = self.trash(actor=actor, strategy=strategy)
        elif self.is_trashed:
            changed = self.remove(actor=actor, strategy=strategy)

        return delete_result(self, 1 if changed else 0)
