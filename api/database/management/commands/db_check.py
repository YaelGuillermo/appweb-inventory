# api/database/management/commands/db_check.py
from django.core.management.base import BaseCommand

from database.services.config import get_postgres_config
from database.services.postgres_admin import database_exists


class Command(BaseCommand):
    help = "Check whether the configured PostgreSQL database exists."

    def handle(self, *args, **options) -> None:
        config = get_postgres_config()
        exists = database_exists(config)
        status = "exists" if exists else "does not exist"
        self.stdout.write(
            self.style.SUCCESS(
                f'[database] Database "{config.name}" {status} at {config.host}:{config.port}.'
            )
        )
