from __future__ import annotations

from core_apps.common.limits.config import LimitConfig


class LimitableModelMixin:
    limit_config: LimitConfig | None = None

    @classmethod
    def get_limit_config(cls) -> LimitConfig | None:
        return cls.limit_config
