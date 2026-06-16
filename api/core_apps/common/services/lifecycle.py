# api/core_apps/common/services/lifecycle.py
from __future__ import annotations

from typing import TYPE_CHECKING

from core_apps.common.choices import LifecycleStrategy

if TYPE_CHECKING:
    from django.db import models


def delete_result(
    instance: models.Model, affected_rows: int
) -> tuple[int, dict[str, int]]:
    """Return the same shape Django's delete API returns."""
    return affected_rows, {instance._meta.label: affected_rows}


def cascade_lifecycle_transition(
    instance: models.Model,
    *,
    action: str,
    actor=None,
    strategy: str | LifecycleStrategy = LifecycleStrategy.SHALLOW,
    **kwargs,
) -> int:
    """
    Apply a lifecycle transition to explicitly declared child querysets.

    Models opt into deep lifecycle behavior by overriding
    `get_lifecycle_children()` and yielding querysets. This avoids hidden magic
    and keeps cascade rules close to the domain model that owns them.
    """
    if LifecycleStrategy(strategy) != LifecycleStrategy.DEEP:
        return 0

    affected_rows = 0

    for child_queryset in instance.get_lifecycle_children():
        transition = getattr(child_queryset, action, None)

        if transition is None:
            continue

        affected_rows += transition(actor=actor, strategy=strategy, **kwargs)

    return affected_rows
