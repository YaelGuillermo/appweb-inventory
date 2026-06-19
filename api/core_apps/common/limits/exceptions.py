from __future__ import annotations

from rest_framework.exceptions import ValidationError

from core_apps.common.limits.snapshots import LimitSnapshot


class LimitExceededError(ValidationError):
    def __init__(self, snapshot: LimitSnapshot, *, units: int = 1) -> None:
        super().__init__(
            {
                "detail": "Creation limit reached.",
                "code": snapshot.reason.value if snapshot.reason else "limit_reached",
                "requested_units": units,
                "limits": snapshot.to_dict(),
            }
        )


class LimitContextError(ValidationError):
    def __init__(self, detail: str, *, code: str) -> None:
        super().__init__({"detail": detail, "code": code})
