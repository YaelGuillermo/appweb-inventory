from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model, QuerySet

from core_apps.common.choices.limits import LimitFailureReason, LimitStrategy
from core_apps.common.limits.config import LimitConfig, LimitLevelRule
from core_apps.common.limits.exceptions import LimitContextError, LimitExceededError
from core_apps.common.limits.snapshots import LimitScope, LimitSnapshot


@dataclass(slots=True)
class LimitContext:
    user: Any = None
    parent_id: str | None = None
    scope_id: str | None = None


class LimitService:
    def get_snapshot(
        self,
        *,
        model: type[Model],
        queryset: QuerySet,
        config: LimitConfig,
        context: LimitContext,
    ) -> LimitSnapshot:
        queryset = self._active_queryset(queryset, config)

        if config.strategy == LimitStrategy.USER:
            return self._user_snapshot(queryset, config, context)

        if config.strategy == LimitStrategy.GLOBAL:
            return self._global_snapshot(queryset, config)

        if config.strategy == LimitStrategy.PARENT:
            return self._parent_snapshot(queryset, config, context)

        if config.strategy == LimitStrategy.TREE:
            return self._tree_snapshot(model, queryset, config, context)

        raise ImproperlyConfigured(f"Unsupported limit strategy: {config.strategy}")

    def assert_can_create(self, snapshot: LimitSnapshot, units: int = 1) -> None:
        if snapshot.current + units <= snapshot.maximum and snapshot.reason is None:
            return

        raise LimitExceededError(snapshot, units=units)

    def _active_queryset(self, queryset: QuerySet, config: LimitConfig) -> QuerySet:
        model_fields = {field.name for field in queryset.model._meta.fields}

        if config.lifecycle_field in model_fields:
            return queryset.filter(**{config.lifecycle_field: config.active_value})

        return queryset

    def _user_snapshot(
        self,
        queryset: QuerySet,
        config: LimitConfig,
        context: LimitContext,
    ) -> LimitSnapshot:
        user = context.user

        if not user or not getattr(user, "is_authenticated", False):
            current = 0
        else:
            current = queryset.filter(**{config.user_field: user}).count()

        return self._build_snapshot(
            current=current,
            maximum=config.maximum,
            strategy=LimitStrategy.USER,
        )

    def _global_snapshot(
        self, queryset: QuerySet, config: LimitConfig
    ) -> LimitSnapshot:
        return self._build_snapshot(
            current=queryset.count(),
            maximum=config.maximum,
            strategy=LimitStrategy.GLOBAL,
        )

    def _parent_snapshot(
        self,
        queryset: QuerySet,
        config: LimitConfig,
        context: LimitContext,
    ) -> LimitSnapshot:
        if not context.parent_id:
            raise LimitContextError(
                "Parent context is required for this limit.",
                code="parent_context_required",
            )

        current = queryset.filter(
            **{f"{config.parent_field}_id": context.parent_id}
        ).count()

        return self._build_snapshot(
            current=current,
            maximum=config.maximum,
            strategy=LimitStrategy.PARENT,
            scope=LimitScope(parent_id=context.parent_id),
        )

    def _tree_snapshot(
        self,
        model: type[Model],
        queryset: QuerySet,
        config: LimitConfig,
        context: LimitContext,
    ) -> LimitSnapshot:
        parent_id = context.parent_id
        level = self._resolve_tree_level(model, config, parent_id)
        max_depth = config.max_depth

        scope = LimitScope(
            level=level,
            max_depth=max_depth,
            parent_id=parent_id,
            scope_field=config.scope_field,
            scope_id=context.scope_id,
        )

        if max_depth is not None and level > max_depth:
            return LimitSnapshot(
                current=0,
                maximum=0,
                strategy=LimitStrategy.TREE,
                reason=LimitFailureReason.TREE_DEPTH_REACHED,
                scope=scope,
            )

        filters = {f"{config.parent_field}_id": parent_id}

        if config.scope_field and context.scope_id:
            filters[f"{config.scope_field}_id"] = context.scope_id

        current = queryset.filter(**filters).count()

        return self._build_snapshot(
            current=current,
            maximum=self._resolve_maximum_for_level(config, level),
            strategy=LimitStrategy.TREE,
            scope=scope,
        )

    def _resolve_tree_level(
        self,
        model: type[Model],
        config: LimitConfig,
        parent_id: str | None,
    ) -> int:
        if not parent_id:
            return 1

        level = 1
        current_parent_id = parent_id
        visited: set[str] = set()

        while current_parent_id:
            if current_parent_id in visited:
                raise LimitContextError(
                    "Cycle detected in tree.",
                    code="tree_cycle_detected",
                )

            visited.add(current_parent_id)

            parent = (
                model.objects.filter(pk=current_parent_id)
                .only("id", config.parent_field)
                .first()
            )

            if not parent:
                break

            current_parent_id = getattr(parent, f"{config.parent_field}_id", None)
            level += 1

            if level > 1000:
                raise LimitContextError(
                    "Tree depth safety limit reached.",
                    code="tree_safety_depth_reached",
                )

        return level

    def _resolve_maximum_for_level(self, config: LimitConfig, level: int) -> int:
        for rule in config.level_limits:
            if self._level_matches(rule, level):
                return rule.maximum

        return config.maximum

    def _level_matches(self, rule: LimitLevelRule, level: int) -> bool:
        if rule.level is not None:
            return rule.level == level

        from_level = rule.from_level if rule.from_level is not None else float("-inf")
        to_level = rule.to_level if rule.to_level is not None else float("inf")

        return from_level <= level <= to_level

    def _build_snapshot(
        self,
        *,
        current: int,
        maximum: int,
        strategy: LimitStrategy,
        scope: LimitScope | None = None,
    ) -> LimitSnapshot:
        reason = None if current < maximum else LimitFailureReason.LIMIT_REACHED

        return LimitSnapshot(
            current=current,
            maximum=maximum,
            strategy=strategy,
            reason=reason,
            scope=scope,
        )
