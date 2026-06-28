# api/core_apps/inventory/admin.py
from django.contrib import admin

from core_apps.inventory.models import WarehouseModel


@admin.register(WarehouseModel)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "city",
        "state",
        "country",
        "is_default",
        "lifecycle_state",
        "created_at",
    )
    list_filter = (
        "lifecycle_state",
        "is_default",
        "country",
        "state",
        "city",
    )
    search_fields = (
        "name",
        "code",
        "address_line",
        "city",
        "state",
        "country",
        "postal_code",
        "reference",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "trashed_at",
        "removed_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "name",
                    "description",
                    "code",
                    "is_default",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "address_line",
                    "city",
                    "state",
                    "country",
                    "postal_code",
                    "reference",
                )
            },
        ),
        (
            "Lifecycle",
            {
                "fields": (
                    "lifecycle_state",
                    "trashed_at",
                    "removed_at",
                )
            },
        ),
        (
            "Audit",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_by",
                    "updated_by",
                    "trashed_by",
                    "removed_by",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
