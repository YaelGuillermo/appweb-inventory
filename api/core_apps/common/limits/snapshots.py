from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core_apps.common.choices.limits import LimitFailureReason, LimitStrategy


@dataclass(frozen=True, slots=True)
class LimitScope:
    level: int | None = None
    max_depth: int | None = None
    parent_id: str | None = None
    scope_field: str | None = None
    scope_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in {
                "level": self.level,
                "max_depth": self.max_depth,
                "parent_id": self.parent_id,
                "scope_field": self.scope_field,
                "scope_id": self.scope_id,
            }.items()
            if value is not None
        }


@dataclass(frozen=True, slots=True)
class LimitSnapshot:
    current: int
    maximum: int
    strategy: LimitStrategy
    reason: LimitFailureReason | None = None
    scope: LimitScope | None = None

    @property
    def remaining(self) -> int:
        return max(0, self.maximum - self.current)

    @property
    def can_create(self) -> bool:
        return self.reason is None and self.current < self.maximum

    def to_dict(self) -> dict[str, Any]:
        return {
            "current": self.current,
            "maximum": self.maximum,
            "remaining": self.remaining,
            "can_create": self.can_create,
            "strategy": self.strategy.value,
            "reason": self.reason.value if self.reason else None,
            "scope": self.scope.to_dict() if self.scope else None,
        }
