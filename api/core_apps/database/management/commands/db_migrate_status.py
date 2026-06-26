# api/core_apps/database/management/commands/db_migrate_status.py
from __future__ import annotations

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Alias for Django showmigrations."

    def add_arguments(self, parser) -> None:
        parser.add_argument("app_label", nargs="*", help="Optional app labels.")

    def handle(self, *args, **options) -> None:
        app_labels = options.get("app_label") or []
        call_command(
            "showmigrations",
            *app_labels,
            verbosity=options.get("verbosity", 1),
        )
