# api/core_apps/database/management/commands/db_reset_schemas.py
from __future__ import annotations

from core_apps.database.management.commands._database_command import SafeDatabaseCommand
from core_apps.database.services.config import get_postgres_config
from core_apps.database.services.postgres_admin import reset_database_schemas


class Command(SafeDatabaseCommand):
    help = "Drop and recreate application schemas. Requires --force."

    def add_arguments(self, parser) -> None:
        self.add_force_argument(parser)
        parser.add_argument(
            "--schemas",
            default=None,
            help="Comma-separated schemas. Defaults to DB_APPLICATION_SCHEMAS.",
        )
        parser.add_argument(
            "--include-public",
            action="store_true",
            help="Allow resetting the public schema too.",
        )

    def handle(self, *args, **options) -> None:
        self.require_force(
            force=options["force"],
            message="This command drops and recreates application schemas.",
        )
        self.protect_production(allow_production=options["allow_production"])

        schemas = None
        if options["schemas"]:
            schemas = [
                schema.strip()
                for schema in options["schemas"].split(",")
                if schema.strip()
            ]

        config = get_postgres_config()
        reset_schemas = reset_database_schemas(
            config,
            schemas,
            include_public=options["include_public"],
        )

        if reset_schemas:
            self.write_success(f"Reset schemas: {', '.join(reset_schemas)}.")
        else:
            self.write_warning(
                "No schemas were reset. Use --include-public if only public is configured."
            )
