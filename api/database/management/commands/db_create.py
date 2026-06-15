# api/database/management/commands/db_create.py
from django.core.management.base import BaseCommand

from database.services.config import get_postgres_config
from database.services.postgres_admin import (
    create_database_if_missing,
    ensure_database_schemas,
)


class Command(BaseCommand):
    help = "Create the configured PostgreSQL database if missing and ensure schemas."

    def handle(self, *args, **options) -> None:
        config = get_postgres_config()
        created = create_database_if_missing(config)
        schemas = ensure_database_schemas(config)

        if created:
            self.stdout.write(self.style.SUCCESS(f'[database] Database "{config.name}" created.'))
        else:
            self.stdout.write(self.style.WARNING(f'[database] Database "{config.name}" already exists.'))

        self.stdout.write(self.style.SUCCESS(f"[database] Schemas ready: {', '.join(schemas)}."))
