# api/database/management/commands/db_seed.py
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from database.management.commands._database_command import SafeDatabaseCommand


class Command(SafeDatabaseCommand):
    help = "Seed database using Django fixtures. Extend this command for model factories."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "fixtures",
            nargs="*",
            help="Fixture names or paths to load with Django loaddata.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Required to load seed data.",
        )

    def handle(self, *args, **options) -> None:
        self.require_force(
            force=options["force"],
            message="This command loads seed data into the database.",
        )

        fixtures = options.get("fixtures") or []
        if not fixtures:
            raise CommandError(
                "No fixtures provided. Example: python manage.py db_seed core_apps/accounts/fixtures/users.json --force"
            )

        call_command("loaddata", *fixtures, verbosity=options.get("verbosity", 1))
        self.write_success(f"Loaded {len(fixtures)} fixture(s).")
