# api/database/management/commands/db_makemigrations.py
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Alias for Django makemigrations."

    def add_arguments(self, parser) -> None:
        parser.add_argument("app_label", nargs="*", help="Optional app labels.")

    def handle(self, *args, **options) -> None:
        app_labels = options.get("app_label") or []
        call_command(
            "makemigrations", *app_labels, verbosity=options.get("verbosity", 1)
        )
