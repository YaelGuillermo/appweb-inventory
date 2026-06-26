# api/core_apps/database/management/commands/db_schemas.py
from __future__ import annotations

from django.core.management.base import BaseCommand

from core_apps.database.services.config import get_postgres_config
from core_apps.database.services.postgres_admin import ensure_database_schemas


class Command(BaseCommand):
    help = "Ensure configured PostgreSQL schemas exist."

    def handle(self, *args, **options) -> None:
        config = get_postgres_config()
        schemas = ensure_database_schemas(config)
        self.stdout.write(
            self.style.SUCCESS(f"[database] Schemas ready: {', '.join(schemas)}.")
        )
