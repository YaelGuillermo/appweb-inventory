# api/core_apps/infrastructure/health/services.py
from __future__ import annotations

import time
from collections.abc import Iterable

from django.conf import settings
from django.utils import timezone

from core_apps.infrastructure.health.checks import (
    CacheHealthCheck,
    DatabaseHealthCheck,
    MemoryHealthCheck,
    StorageHealthCheck,
)
from core_apps.infrastructure.health.types import (
    HealthCheckKind,
    HealthIndicatorResult,
    HealthReport,
)

_STARTED_AT = time.time()


class HealthService:
    def liveness(self) -> HealthReport:
        return self.build_report(
            kind="liveness",
            checks=[MemoryHealthCheck().check(include_details=self.include_details)],
        )

    def readiness(self) -> HealthReport:
        checks = [
            DatabaseHealthCheck().check(include_details=self.include_details),
            CacheHealthCheck().check(include_details=self.include_details),
            StorageHealthCheck().check(include_details=self.include_details),
        ]
        return self.build_report(kind="readiness", checks=checks)

    def full(self) -> HealthReport:
        checks = [
            MemoryHealthCheck().check(include_details=self.include_details),
            DatabaseHealthCheck().check(include_details=self.include_details),
            CacheHealthCheck().check(include_details=self.include_details),
            StorageHealthCheck().check(include_details=self.include_details),
        ]
        return self.build_report(kind="full", checks=checks)

    @property
    def include_details(self) -> bool:
        return bool(getattr(settings, "HEALTH_CHECK_DETAILS_ENABLED", False))

    def build_report(
        self,
        *,
        kind: HealthCheckKind,
        checks: Iterable[HealthIndicatorResult],
    ) -> HealthReport:
        checks_list = list(checks)
        has_down_check = any(check.status == "down" for check in checks_list)

        return HealthReport(
            status="error" if has_down_check else "ok",
            kind=kind,
            timestamp=timezone.now().isoformat(),
            uptime_seconds=max(0, round(time.time() - _STARTED_AT)),
            service={
                "name": getattr(settings, "SITE_NAME", "Site"),
                "environment": getattr(settings, "ENVIRONMENT", "development"),
                "api_version": getattr(settings, "API_VERSION", "v1"),
            },
            checks=checks_list,
        )
