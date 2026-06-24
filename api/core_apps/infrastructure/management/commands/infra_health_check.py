# api/core_apps/infrastructure/management/commands/infra_health_check.py
from __future__ import annotations

import json

from django.core.management.base import BaseCommand, CommandError

from core_apps.infrastructure.health.services import HealthService


class Command(BaseCommand):
    help = "Run infrastructure health checks from the command line."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--kind",
            choices=["liveness", "readiness", "full"],
            default="full",
            help="Health check group to run.",
        )
        parser.add_argument(
            "--json",
            action="store_true",
            help="Print machine-readable JSON output.",
        )

    def handle(self, *args, **options) -> None:
        service = HealthService()
        kind = options["kind"]

        if kind == "liveness":
            report = service.liveness()
        elif kind == "readiness":
            report = service.readiness()
        else:
            report = service.full()

        payload = report.as_dict()
        if options["json"]:
            self.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            self.stdout.write(f"[infra] {kind}: {payload['status']}")
            for check in payload["checks"]:
                self.stdout.write(
                    f"[infra] - {check['name']}: {check['status']} ({check['latency_ms']}ms)"
                )

        if payload["status"] != "ok":
            raise CommandError("Infrastructure health check failed.")
