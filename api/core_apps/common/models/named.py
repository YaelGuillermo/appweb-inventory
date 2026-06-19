from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.common.constants import DESCRIPTION_MAX_LENGTH, NAME_MAX_LENGTH
from core_apps.common.normalizers import normalize_human_name
from core_apps.common.validators import validate_name_rules

from .base import BaseModel


class NamedModel(BaseModel):
    """Abstract model for business records with a human-readable name."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        db_index=True,
        verbose_name=_("Name"),
        help_text=_("Human-readable name of this record."),
        validators=[validate_name_rules],
        error_messages={
            "blank": _("The name cannot be blank."),
            "max_length": _("The name cannot exceed %(limit_value)s characters."),
        },
    )
    description = models.TextField(
        max_length=DESCRIPTION_MAX_LENGTH,
        blank=True,
        null=True,
        default=None,
        verbose_name=_("Description"),
        help_text=_("Optional short description."),
    )

    class Meta(BaseModel.Meta):
        abstract = True
        verbose_name = _("Named entity")
        verbose_name_plural = _("Named entities")
        ordering = ["name"]
        indexes = [
            *BaseModel.Meta.indexes,
            models.Index(
                fields=["name"],
                name="%(app_label)s_%(class)s_name_idx",
            ),
        ]

    def clean(self) -> None:
        super().clean()
        self.name = normalize_human_name(self.name)

    def __str__(self) -> str:
        return self.name
