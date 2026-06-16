# api/localization/management/commands/locale_compile.py
from django.core.management import call_command

from localization.management.commands._locale_command import LocaleCommand
from localization.services.paths import working_directory


class Command(LocaleCommand):
    help = "Compile per-app .po files into .mo files."

    def add_arguments(self, parser) -> None:
        self.add_common_arguments(parser)
        parser.add_argument(
            "--use-fuzzy",
            action="store_true",
            help="Include fuzzy translations when compiling.",
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
            if not target.locale_path.exists():
                self.write_warning(f"Skipping {target.name}: locale directory missing.")
                continue

            ignore_patterns = self.get_ignore_patterns_for_target(target)

            for locale in locales:
                self.write_success(f"Compiling messages for {target.name} [{locale}].")

                with working_directory(target.path):
                    call_command(
                        "compilemessages",
                        locale=[locale],
                        ignore_patterns=ignore_patterns,
                        use_fuzzy=options["use_fuzzy"],
                        verbosity=options.get("verbosity", 1),
                    )

        self.write_success("Message files compiled.")
