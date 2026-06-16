# api/localization/apps.py
from django.apps import AppConfig


class LocalizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "localization"
    label = "localization"
    verbose_name = "Localization Utilities"
