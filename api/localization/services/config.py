# api/localization/services/config.py
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import to_locale


@dataclass(frozen=True, slots=True)
class LocalizationTarget:
    name: str
    path: Path
    locale_path: Path
    is_global: bool = False
    extra_ignore_patterns: tuple[str, ...] = field(default_factory=tuple)


def normalize_locale_code(language_code: str) -> str:
    """Convert Django language codes to gettext locale codes."""
    return to_locale(language_code.strip())


def normalize_language_code(locale_code: str) -> str:
    """Convert gettext locale codes to Django language codes."""
    return locale_code.strip().replace("_", "-").lower()


def get_base_language_code() -> str:
    return normalize_locale_code(settings.LANGUAGE_CODE)


def get_configured_locale_codes(*, include_base: bool = False) -> list[str]:
    base_language = get_base_language_code()
    locales: list[str] = []

    for language_code, _label in settings.LANGUAGES:
        locale = normalize_locale_code(language_code)

        if not include_base and locale == base_language:
            continue

        if locale not in locales:
            locales.append(locale)

    return locales


def get_ignore_patterns() -> list[str]:
    return list(
        getattr(
            settings,
            "I18N_IGNORE_PATTERNS",
            [
                "venv/*",
                "env/*",
                ".venv/*",
                "staticfiles/*",
                "media/*",
                "logs/*",
                "__pycache__/*",
                "*.pyc",
            ],
        )
    )


def get_core_apps_dir() -> Path:
    return Path(settings.BASE_DIR) / "core_apps"


def discover_core_apps() -> list[str]:
    core_apps_dir = get_core_apps_dir()

    if not core_apps_dir.exists():
        return []

    app_names: list[str] = []

    for path in sorted(core_apps_dir.iterdir()):
        if not path.is_dir():
            continue

        if path.name.startswith("__"):
            continue

        if (path / "apps.py").exists():
            app_names.append(path.name)

    return app_names


def resolve_app_names(
    *,
    apps: str | None = None,
    all_apps: bool = False,
) -> list[str]:
    if apps:
        return [app.strip() for app in apps.split(",") if app.strip()]

    if all_apps:
        return discover_core_apps()

    return discover_core_apps()


def resolve_locales(locales: str | None = None) -> list[str]:
    if locales:
        return [
            normalize_locale_code(locale)
            for locale in locales.split(",")
            if locale.strip()
        ]

    return get_configured_locale_codes(include_base=False)


def resolve_targets(
    *,
    apps: str | None = None,
    all_apps: bool = False,
    include_global: bool = False,
    global_only: bool = False,
) -> list[LocalizationTarget]:
    base_dir = Path(settings.BASE_DIR)
    targets: list[LocalizationTarget] = []

    if include_global or global_only:
        targets.append(
            LocalizationTarget(
                name="global",
                path=base_dir,
                locale_path=base_dir / "locale",
                is_global=True,
                extra_ignore_patterns=(
                    "core_apps/*",
                    "database/*",
                    "localization/*",
                ),
            )
        )

    if global_only:
        return targets

    for app_name in resolve_app_names(apps=apps, all_apps=all_apps):
        app_path = get_core_apps_dir() / app_name

        if not app_path.exists():
            raise ImproperlyConfigured(
                f'Core app "{app_name}" does not exist at {app_path}.'
            )

        if not (app_path / "apps.py").exists():
            raise ImproperlyConfigured(
                f'Core app "{app_name}" must contain an apps.py file.'
            )

        targets.append(
            LocalizationTarget(
                name=app_name,
                path=app_path,
                locale_path=app_path / "locale",
                is_global=False,
            )
        )

    return targets
