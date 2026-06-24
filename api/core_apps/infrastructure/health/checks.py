# api/core_apps/infrastructure/health/checks.py
from __future__ import annotations

import gc
import os
import resource
import time
from typing import Any
from uuid import uuid4

from django.conf import settings
from django.core.cache import caches
from django.db import connections

from core_apps.infrastructure.health.types import HealthIndicatorResult
from core_apps.infrastructure.storage.services import MediaStorageService


def elapsed_ms(started_at: float) -> int:
    return max(0, round((time.perf_counter() - started_at) * 1000))


def serialize_error(error: Exception) -> dict[str, str]:
    return {
        "type": error.__class__.__name__,
        "message": str(error),
    }


class MemoryHealthCheck:
    name = "memory"

    def check(self, *, include_details: bool) -> HealthIndicatorResult:
        started_at = time.perf_counter()
        usage = resource.getrusage(resource.RUSAGE_SELF)

        details: dict[str, Any] | None = None
        if include_details:
            details = {
                "pid": os.getpid(),
                "gc_counts": list(gc.get_count()),
                "max_rss_kb": int(getattr(usage, "ru_maxrss", 0)),
            }

        return HealthIndicatorResult(
            name=self.name,
            status="up",
            latency_ms=elapsed_ms(started_at),
            details=details,
        )


class DatabaseHealthCheck:
    name = "database"

    def __init__(self, *, alias: str = "default") -> None:
        self.alias = alias

    def check(self, *, include_details: bool) -> HealthIndicatorResult:
        started_at = time.perf_counter()

        try:
            connection = connections[self.alias]
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

            details: dict[str, Any] | None = None
            if include_details:
                database_settings = settings.DATABASES.get(self.alias, {})
                details = {
                    "alias": self.alias,
                    "vendor": connection.vendor,
                    "host": database_settings.get("HOST"),
                    "port": database_settings.get("PORT"),
                    "name": database_settings.get("NAME"),
                }

            return HealthIndicatorResult(
                name=self.name,
                status="up",
                latency_ms=elapsed_ms(started_at),
                details=details,
            )
        except Exception as error:
            return HealthIndicatorResult(
                name=self.name,
                status="down",
                latency_ms=elapsed_ms(started_at),
                details=serialize_error(error) if include_details else None,
            )


class CacheHealthCheck:
    name = "cache"

    def __init__(self, *, alias: str = "default") -> None:
        self.alias = alias

    def check(self, *, include_details: bool) -> HealthIndicatorResult:
        started_at = time.perf_counter()
        key = f"infrastructure:health:{uuid4()}"

        try:
            cache = caches[self.alias]
            cache.set(key, "ok", timeout=5)
            value = cache.get(key)
            cache.delete(key)

            if value != "ok":
                raise RuntimeError("Cache write/read check failed.")

            details: dict[str, Any] | None = None
            if include_details:
                backend = settings.CACHES.get(self.alias, {}).get("BACKEND")
                details = {
                    "alias": self.alias,
                    "backend": backend,
                }

            return HealthIndicatorResult(
                name=self.name,
                status="up",
                latency_ms=elapsed_ms(started_at),
                details=details,
            )
        except Exception as error:
            return HealthIndicatorResult(
                name=self.name,
                status="down",
                latency_ms=elapsed_ms(started_at),
                details=serialize_error(error) if include_details else None,
            )


class StorageHealthCheck:
    name = "storage"

    def __init__(self, *, storage: MediaStorageService | None = None) -> None:
        self.storage = storage or MediaStorageService()

    def check(self, *, include_details: bool) -> HealthIndicatorResult:
        started_at = time.perf_counter()

        try:
            self.storage.assert_healthy()
            return HealthIndicatorResult(
                name=self.name,
                status="up",
                latency_ms=elapsed_ms(started_at),
                details=self.storage.get_runtime_details() if include_details else None,
            )
        except Exception as error:
            details = serialize_error(error) if include_details else None
            if details is not None:
                details["driver"] = self.storage.driver

            return HealthIndicatorResult(
                name=self.name,
                status="down",
                latency_ms=elapsed_ms(started_at),
                details=details,
            )
