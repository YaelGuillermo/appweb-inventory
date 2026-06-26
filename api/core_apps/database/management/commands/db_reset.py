# api/core_apps/database/management/commands/db_reset.py
from __future__ import annotations

from core_apps.database.management.commands._database_command import SafeDatabaseCommand
from core_apps.database.services.config import get_postgres_config
from core_apps.database.services.postgres_admin import (
    create_database_if_missing,
    drop_database_if_exists,
    ensure_database_schemas,
)


class Command(SafeDatabaseCommand):
    help = "Drop and recreate the configured PostgreSQL database. Requires --force."

    def add_arguments(self, parser) -> None:
        self.add_force_argument(parser)

    def handle(self, *args, **options) -> None:
        self.require_force(
            force=options["force"],
            message="This command drops and recreates the configured database.",
        )
        self.protect_production(allow_production=options["allow_production"])

        config = get_postgres_config()
        drop_database_if_exists(config)
        create_database_if_missing(config)
        schemas = ensure_database_schemas(config)

        self.write_success(f'Database "{config.name}" reset.')
        self.write_success(f"Schemas ready: {', '.join(schemas)}.")
