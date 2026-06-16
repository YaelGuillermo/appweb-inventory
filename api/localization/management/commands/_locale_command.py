# api/localization/management/commands/_locale_command.py
from __future__ import annotations

from django.core.management.base import BaseCommand

from localization.services.config import (
    get_ignore_patterns,
    resolve_locales,
    resolve_targets,
)


class LocaleCommand(BaseCommand):
    prefix = "locale"

    def add_common_arguments(self, parser) -> None:
        parser.add_argument(
            "--apps",
            default=None,
            help=(
                "Comma-separated core app names. "
                "Example: --apps=common,accounts,projects"
            ),
        )
        parser.add_argument(
            "--all-apps",
            action="store_true",
            help="Use every app folder inside core_apps that contains apps.py.",
        )
        parser.add_argument(
            "--locales",
            default=None,
            help=(
                "Comma-separated gettext locales. "
                "Defaults to LANGUAGES excluding the base language."
            ),
        )
        parser.add_argument(
            "--include-global",
            action="store_true",
            help="Also process BASE_DIR/locale for global project translations.",
        )
        parser.add_argument(
            "--global-only",
            action="store_true",
            help="Process only BASE_DIR/locale and skip core_apps.",
        )

    def get_targets_from_options(self, options):
        return resolve_targets(
            apps=options.get("apps"),
            all_apps=options.get("all_apps", False),
            include_global=options.get("include_global", False),
            global_only=options.get("global_only", False),
        )

    def get_locales_from_options(self, options) -> list[str]:
        return resolve_locales(options.get("locales"))

    def get_ignore_patterns(self) -> list[str]:
        return get_ignore_patterns()

    def get_ignore_patterns_for_target(self, target) -> list[str]:
        return [*self.get_ignore_patterns(), *target.extra_ignore_patterns]

    def write_success(self, message: str) -> None:
        self.stdout.write(self.style.SUCCESS(f"[locale] {message}"))

    def write_warning(self, message: str) -> None:
        self.stdout.write(self.style.WARNING(f"[locale] {message}"))
