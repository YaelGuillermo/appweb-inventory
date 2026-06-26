# api/core_apps/database/management/commands/db_truncate.py
from __future__ import annotations

from core_apps.database.management.commands._database_command import SafeDatabaseCommand
from core_apps.database.services.config import get_postgres_config
from core_apps.database.services.table_maintenance import truncate_database_tables


class Command(SafeDatabaseCommand):
    help = "Truncate application database tables without dropping schema. Requires --force."

    def add_arguments(self, parser) -> None:
        self.add_force_argument(parser)
        parser.add_argument(
            "--schemas",
            default=None,
            help="Comma-separated schemas. Defaults to DB_APPLICATION_SCHEMAS.",
        )
        parser.add_argument(
            "--include-migrations",
            action="store_true",
            help="Also truncate django_migrations.",
        )

    def handle(self, *args, **options) -> None:
        self.require_force(
            force=options["force"],
            message="This command truncates data from database tables.",
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
        tables = truncate_database_tables(
            config,
            schemas,
            include_migrations_table=options["include_migrations"],
        )

        if tables:
            self.write_success(f"Truncated {len(tables)} table(s).")
        else:
            self.write_warning("No tables found to truncate.")
