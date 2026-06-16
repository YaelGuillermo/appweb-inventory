# api/core_apps/common/querysets/lifecycle.py
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db import models
from django.utils import timezone

from core_apps.common.choices import LifecycleState, LifecycleStrategy

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser


class LifecycleQuerySet(models.QuerySet):
    """Chainable queryset API for two-step logical lifecycle transitions."""

    def active(self):
        return self.filter(lifecycle_state=LifecycleState.ACTIVE)

    def trashed(self):
        return self.filter(lifecycle_state=LifecycleState.TRASHED)

    def removed(self):
        return self.filter(lifecycle_state=LifecycleState.REMOVED)

    def not_removed(self):
        return self.exclude(lifecycle_state=LifecycleState.REMOVED)

    def visible_to_user(self):
        return self.active()

    def visible_in_trash(self):
        return self.trashed()

    def visible_to_admin(self):
        return self.all()

    def with_lifecycle_state(self, state: str | LifecycleState):
        return self.filter(lifecycle_state=LifecycleState(state))

    def trash(
        self,
        *,
        actor: AbstractBaseUser | None = None,
        strategy: str | LifecycleStrategy = LifecycleStrategy.SHALLOW,
    ) -> int:
        """First deletion: move active records into the user's trash."""
        strategy = LifecycleStrategy(strategy)

        if strategy == LifecycleStrategy.DEEP:
            return sum(
                instance.trash(actor=actor, strategy=strategy)
                for instance in self.active().iterator()
            )

        now = timezone.now()
        update_fields: dict[str, Any] = {
            "lifecycle_state": LifecycleState.TRASHED,
            "trashed_at": now,
            "removed_at": None,
            "removed_by": None,
            "updated_at": now,
        }

        if actor is not None:
            update_fields["trashed_by"] = actor
            update_fields["updated_by"] = actor

        return self.active().update(**update_fields)

    def remove(
        self,
        *,
        actor: AbstractBaseUser | None = None,
        strategy: str | LifecycleStrategy = LifecycleStrategy.SHALLOW,
    ) -> int:
        """Second deletion: hide trashed records from user-facing flows."""
        strategy = LifecycleStrategy(strategy)

        if strategy == LifecycleStrategy.DEEP:
            return sum(
                instance.remove(actor=actor, strategy=strategy)
                for instance in self.trashed().iterator()
            )

        now = timezone.now()
        update_fields: dict[str, Any] = {
            "lifecycle_state": LifecycleState.REMOVED,
            "removed_at": now,
            "updated_at": now,
        }

        if actor is not None:
            update_fields["removed_by"] = actor
            update_fields["updated_by"] = actor

        return self.trashed().update(**update_fields)

    def restore(
        self,
        *,
        actor: AbstractBaseUser | None = None,
        include_removed: bool = False,
        strategy: str | LifecycleStrategy = LifecycleStrategy.SHALLOW,
    ) -> int:
        """
        Restore records to active.

        User-facing flows restore only trashed records. Admin/system flows may
        pass `include_removed=True` to recover second-level removed records.
        """
        strategy = LifecycleStrategy(strategy)
        queryset = self.all() if include_removed else self.trashed()
        queryset = queryset.exclude(lifecycle_state=LifecycleState.ACTIVE)

        if strategy == LifecycleStrategy.DEEP:
            return sum(
                instance.restore(
                    actor=actor,
                    include_removed=include_removed,
                    strategy=strategy,
                )
                for instance in queryset.iterator()
            )

        now = timezone.now()
        update_fields: dict[str, Any] = {
            "lifecycle_state": LifecycleState.ACTIVE,
            "trashed_at": None,
            "trashed_by": None,
            "removed_at": None,
            "removed_by": None,
            "updated_at": now,
        }

        if actor is not None:
            update_fields["updated_by"] = actor

        return queryset.update(**update_fields)

    def hard_delete(self) -> tuple[int, dict[str, int]]:
        """Physically delete records. Reserve for exceptional maintenance tasks."""
        return super().delete()

    def delete(
        self,
        *,
        actor: AbstractBaseUser | None = None,
        strategy: str | LifecycleStrategy = LifecycleStrategy.SHALLOW,
        hard: bool = False,
    ) -> tuple[int, dict[str, int]]:
        """
        Advance records one lifecycle level.

        Active records become trashed. Trashed records become removed. Removed
        records remain stored unless `hard=True` is passed explicitly.
        """
        if hard:
            return self.hard_delete()

        removed_count = self.trashed().remove(actor=actor, strategy=strategy)
        trashed_count = self.active().trash(actor=actor, strategy=strategy)
        affected_rows = trashed_count + removed_count

        return affected_rows, {self.model._meta.label: affected_rows}
