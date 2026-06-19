from __future__ import annotations

from dataclasses import dataclass, field

from core_apps.common.choices.limits import LimitStrategy


@dataclass(frozen=True, slots=True)
class LimitLevelRule:
    maximum: int
    level: int | None = None
    from_level: int | None = None
    to_level: int | None = None


@dataclass(frozen=True, slots=True)
class LimitConfig:
    strategy: LimitStrategy
    maximum: int
    user_field: str = "created_by"
    parent_field: str = "parent"
    scope_field: str | None = None
    lifecycle_field: str = "lifecycle_state"
    active_value: str = "active"
    max_depth: int | None = None
    level_limits: tuple[LimitLevelRule, ...] = field(default_factory=tuple)
