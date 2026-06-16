# api/localization/management/commands/locale_make.py
from django.core.management import call_command

from localization.management.commands._locale_command import LocaleCommand
from localization.services.paths import working_directory


class Command(LocaleCommand):
    help = "Generate per-app .po translation files using Django makemessages."

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

    def handle(self, *args, **options) -> None:
        locales = self.get_locales_from_options(options)
        targets = self.get_targets_from_options(options)

        if not locales:
            self.write_warning("No locales configured.")
            return

        if not targets:
            self.write_warning("No localization targets found.")
            return

        for target in targets:
            target.locale_path.mkdir(parents=True, exist_ok=True)
            ignore_patterns = self.get_ignore_patterns_for_target(target)

            for locale in locales:
                self.write_success(f"Generating messages for {target.name} [{locale}].")

                with working_directory(target.path):
                    call_command(
                        "makemessages",
                        locale=[locale],
                        ignore_patterns=ignore_patterns,
                        no_location=options["no_location"],
                        no_obsolete=options["no_obsolete"],
                        verbosity=options.get("verbosity", 1),
                    )

        self.write_success("Message files generated.")
