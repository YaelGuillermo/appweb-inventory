# api/localization/management/commands/locale_refresh.py
from django.core.management import call_command

from localization.management.commands._locale_command import LocaleCommand


class Command(LocaleCommand):
    help = "Generate and compile localization files."

    def add_arguments(self, parser) -> None:
        self.add_common_arguments(parser)
        parser.add_argument(
            "--no-location",
            action="store_true",
            help="Do not write file and line comments into .po files.",
        )
        parser.add_argument(
            "--no-obsolete",
            action="store_true",
            help="Remove obsolete message strings.",
        )
        parser.add_argument(
            "--use-fuzzy",
            action="store_true",
            help="Include fuzzy translations when compiling.",
        )

    def handle(self, *args, **options) -> None:
        common_options = {
            "apps": options.get("apps"),
            "all_apps": options.get("all_apps", False),
            "locales": options.get("locales"),
            "include_global": options.get("include_global", False),
            "global_only": options.get("global_only", False),
            "verbosity": options.get("verbosity", 1),
        }

        call_command(
            "locale_make",
            no_location=options["no_location"],
            no_obsolete=options["no_obsolete"],
            **common_options,
        )

        call_command(
            "locale_compile",
            use_fuzzy=options["use_fuzzy"],
            **common_options,
        )

        self.write_success("Localization refreshed.")
