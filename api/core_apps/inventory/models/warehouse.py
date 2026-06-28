# api/core_apps/inventory/models/warehouse.py
from __future__ import annotations

from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import NamedModel
from core_apps.common.normalizers import normalize_human_name

WAREHOUSE_CODE_MAX_LENGTH = 32
WAREHOUSE_ADDRESS_MAX_LENGTH = 255
WAREHOUSE_CITY_MAX_LENGTH = 128
WAREHOUSE_STATE_MAX_LENGTH = 128
WAREHOUSE_COUNTRY_MAX_LENGTH = 128
WAREHOUSE_POSTAL_CODE_MAX_LENGTH = 20
WAREHOUSE_REFERENCE_MAX_LENGTH = 255


def normalize_warehouse_code(value: str | None) -> str | None:
    normalized = str(value or "").strip().upper()
    return normalized or None


def normalize_optional_name(value: str | None) -> str | None:
    normalized = normalize_human_name(value)
    return normalized or None


class WarehouseModel(NamedModel):
    """
    Physical place where inventory will be located.

    This model intentionally does not include products, stock, movements,
    transactions, or costing rules yet. It is only the inventory location root.
    """

    code = models.CharField(
        max_length=WAREHOUSE_CODE_MAX_LENGTH,
        null=True,
        blank=True,
        default=None,
        db_index=True,
        verbose_name=_("Code"),
        help_text=_("Optional internal code for this warehouse."),
    )
    address_line = models.CharField(
        max_length=WAREHOUSE_ADDRESS_MAX_LENGTH,
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Address"),
        help_text=_("Street, building, campus, room, or physical address."),
    )
    city = models.CharField(
        max_length=WAREHOUSE_CITY_MAX_LENGTH,
        null=True,
        blank=True,
        default=None,
        db_index=True,
        verbose_name=_("City"),
    )
    state = models.CharField(
        max_length=WAREHOUSE_STATE_MAX_LENGTH,
        null=True,
        blank=True,
        default=None,
        db_index=True,
        verbose_name=_("State"),
    )
    country = models.CharField(
        max_length=WAREHOUSE_COUNTRY_MAX_LENGTH,
        null=True,
        blank=True,
        default=None,
        db_index=True,
        verbose_name=_("Country"),
    )
    postal_code = models.CharField(
        max_length=WAREHOUSE_POSTAL_CODE_MAX_LENGTH,
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Postal code"),
    )
    reference = models.CharField(
        max_length=WAREHOUSE_REFERENCE_MAX_LENGTH,
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Reference"),
        help_text=_("Optional location reference, such as floor, gate, or notes."),
    )
    is_default = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Default warehouse"),
        help_text=_("Marks this warehouse as a preferred default option."),
    )

    class Meta(NamedModel.Meta):
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")
        ordering = ["name"]
        indexes = [
            *NamedModel.Meta.indexes,
            models.Index(
                fields=["code"],
                name="%(app_label)s_%(class)s_code_idx",
            ),
            models.Index(
                fields=["country", "state", "city"],
                name="%(app_label)s_%(class)s_location_idx",
            ),
            models.Index(
                fields=["is_default", "name"],
                name="%(app_label)s_%(class)s_default_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="inventory_warehouse_name_ci_uniq",
            ),
            models.UniqueConstraint(
                fields=["code"],
                condition=Q(code__isnull=False),
                name="inventory_warehouse_code_uniq",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        self.code = normalize_warehouse_code(self.code)
        self.address_line = normalize_optional_name(self.address_line)
        self.city = normalize_optional_name(self.city)
        self.state = normalize_optional_name(self.state)
        self.country = normalize_optional_name(self.country)
        self.postal_code = normalize_optional_name(self.postal_code)
        self.reference = normalize_optional_name(self.reference)
