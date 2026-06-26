# api/core_apps/database/management/commands/_database_command.py
from __future__ import annotations

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class SafeDatabaseCommand(BaseCommand):
    destructive_operation = False

    def add_force_argument(self, parser) -> None:
        parser.add_argument(
            "--force",
            action="store_true",
            help="Required for destructive database operations.",
        )
        parser.add_argument(
            "--allow-production",
            action="store_true",
            help="Allow command to run when DJANGO_DEBUG=False.",
        )

    def require_force(self, *, force: bool, message: str) -> None:
        if not force:
            raise CommandError(f"{message}\nRe-run with --force if you are sure.")

    def protect_production(self, *, allow_production: bool) -> None:
        if not getattr(settings, "DEBUG", False) and not allow_production:
            raise CommandError(
                "Refusing to run a destructive command with DEBUG=False. "
                "Pass --allow-production only if you really know what you are doing."
            )

    def write_success(self, message: str) -> None:
        self.stdout.write(self.style.SUCCESS(f"[database] {message}"))

    def write_warning(self, message: str) -> None:
        self.stdout.write(self.style.WARNING(f"[database] {message}"))
