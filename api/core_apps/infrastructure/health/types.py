# api/core_apps/infrastructure/health/types.py
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

HealthIndicatorStatus = Literal["up", "down"]
HealthReportStatus = Literal["ok", "error"]
HealthCheckKind = Literal["liveness", "readiness", "full"]


@dataclass(frozen=True, slots=True)
class HealthIndicatorResult:
    name: str
    status: HealthIndicatorStatus
    latency_ms: int
    details: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if payload.get("details") is None:
            payload.pop("details", None)
        return payload


@dataclass(frozen=True, slots=True)
class HealthReport:
    status: HealthReportStatus
    kind: HealthCheckKind
    timestamp: str
    uptime_seconds: int
    service: dict[str, Any]
    checks: list[HealthIndicatorResult]

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "kind": self.kind,
            "timestamp": self.timestamp,
            "uptime_seconds": self.uptime_seconds,
            "service": self.service,
            "checks": [check.as_dict() for check in self.checks],
        }
