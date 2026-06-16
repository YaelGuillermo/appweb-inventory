# api/database/management/commands/db_migrate.py
from django.core.management import call_command
from django.core.management.base import BaseCommand

from database.services.config import get_postgres_config
from database.services.postgres_admin import ensure_database_schemas


class Command(BaseCommand):
    help = "Ensure schemas and run Django migrations."

    def add_arguments(self, parser) -> None:
        parser.add_argument("app_label", nargs="?", default=None)
        parser.add_argument("migration_name", nargs="?", default=None)

    def handle(self, *args, **options) -> None:
        config = get_postgres_config()
        schemas = ensure_database_schemas(config)
        self.stdout.write(
            self.style.SUCCESS(f"[database] Schemas ready: {', '.join(schemas)}.")
        )

        command_args = []
        if options.get("app_label"):
            command_args.append(options["app_label"])
        if options.get("migration_name"):
            command_args.append(options["migration_name"])

        call_command("migrate", *command_args, verbosity=options.get("verbosity", 1))
