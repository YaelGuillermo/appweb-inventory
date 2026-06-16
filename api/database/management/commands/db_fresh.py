# api/database/management/commands/db_fresh.py
from django.core.management import call_command

from database.management.commands._database_command import SafeDatabaseCommand
from database.services.config import get_postgres_config
from database.services.postgres_admin import (
    create_database_if_missing,
    drop_database_if_exists,
    ensure_database_schemas,
)


class Command(SafeDatabaseCommand):
    help = "Fresh database: drop, create, ensure schemas, and run migrations. Requires --force."

    def add_arguments(self, parser) -> None:
        self.add_force_argument(parser)
        parser.add_argument(
            "--skip-migrations",
            action="store_true",
            help="Do not run Django migrations after recreating the database.",
        )

    def handle(self, *args, **options) -> None:
        self.require_force(
            force=options["force"],
            message="This command completely resets your configured database.",
        )
        self.protect_production(allow_production=options["allow_production"])

        config = get_postgres_config()
        drop_database_if_exists(config)
        create_database_if_missing(config)
        schemas = ensure_database_schemas(config)

        self.write_success(f'Database "{config.name}" recreated.')
        self.write_success(f"Schemas ready: {', '.join(schemas)}.")

        if options["skip_migrations"]:
            self.write_warning("Skipped migrations.")
            return

        call_command(
            "migrate", interactive=False, verbosity=options.get("verbosity", 1)
        )
        self.write_success("Fresh database is ready.")
