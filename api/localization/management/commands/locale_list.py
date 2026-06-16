# api/localization/management/commands/locale_list.py
from localization.management.commands._locale_command import LocaleCommand


class Command(LocaleCommand):
    help = "List configured localization targets and locales."

    def add_arguments(self, parser) -> None:
        self.add_common_arguments(parser)

    def handle(self, *args, **options) -> None:
        locales = self.get_locales_from_options(options)
        targets = self.get_targets_from_options(options)

        self.write_success(f"Locales: {', '.join(locales) or 'none'}")

        if not targets:
            self.write_warning("No localization targets found.")
            return

        for target in targets:
            kind = "global" if target.is_global else "core app"
            self.stdout.write(f"- {target.name} ({kind}) -> {target.locale_path}")
