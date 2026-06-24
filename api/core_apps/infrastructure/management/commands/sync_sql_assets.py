# api/core_apps/infrastructure/management/commands/sync_sql_assets.py
from __future__ import annotations

import json

from django.core.management.base import BaseCommand

from core_apps.infrastructure.sql_assets.sync import sync_sql_assets
from core_apps.infrastructure.sql_assets.types import SqlAssetSyncOptions


class Command(BaseCommand):
    help = "Synchronize registered SQL assets and track checksums."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--force",
            action="store_true",
            help="Execute assets even when their checksum did not change.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would run without executing SQL.",
        )
        parser.add_argument(
            "--include-disabled",
            action="store_true",
            help="Also include assets with enabled=False.",
        )
        parser.add_argument(
            "--manifest",
            default=None,
            help="Python import path containing SQL_ASSETS_MANIFEST.",
        )
        parser.add_argument(
            "--registry-schema",
            default=None,
            help="Schema where sql_assets_registry is stored. Defaults to DB_SCHEMA.",
        )
        parser.add_argument(
            "--json",
            action="store_true",
            help="Print machine-readable JSON output.",
        )

    def handle(self, *args, **options) -> None:
        results = sync_sql_assets(
            options=SqlAssetSyncOptions(
                force=options["force"],
                dry_run=options["dry_run"],
                include_disabled=options["include_disabled"],
            ),
            manifest_module=options["manifest"],
            registry_schema=options["registry_schema"],
        )

        payload = [result.as_dict() for result in results]
        if options["json"]:
            self.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False))
            return

        if not payload:
            self.stdout.write(
                self.style.WARNING("[sql_assets] No SQL assets registered.")
            )
            return

        for item in payload:
            self.stdout.write(
                self.style.SUCCESS(
                    f"[sql_assets] {item['status']}: {item['key']} ({item['kind']})"
                )
            )
