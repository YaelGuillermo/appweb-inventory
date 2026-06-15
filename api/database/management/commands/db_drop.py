# api/database/management/commands/db_drop.py
from database.management.commands._database_command import SafeDatabaseCommand
from database.services.config import get_postgres_config
from database.services.postgres_admin import drop_database_if_exists


class Command(SafeDatabaseCommand):
    help = "Drop the configured PostgreSQL database. Requires --force."

    def add_arguments(self, parser) -> None:
        self.add_force_argument(parser)

    def handle(self, *args, **options) -> None:
        self.require_force(
            force=options["force"],
            message="This command drops the configured database.",
        )
        self.protect_production(allow_production=options["allow_production"])

        config = get_postgres_config()
        dropped = drop_database_if_exists(config)

        if dropped:
            self.write_success(f'Database "{config.name}" dropped.')
        else:
            self.write_warning(f'Database "{config.name}" did not exist.')
