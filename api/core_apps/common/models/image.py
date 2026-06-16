# api/core_apps/common/models/image.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from .stored_file import StoredFileModel


class ImageModel(StoredFileModel):
    """Abstract model for stored image metadata."""

    width = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Width"),
        help_text=_("Image width in pixels."),
    )
    height = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Height"),
        help_text=_("Image height in pixels."),
    )

    class Meta(StoredFileModel.Meta):
        abstract = True
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        indexes = [
            *StoredFileModel.Meta.indexes,
            models.Index(
                fields=["width", "height"],
                name="%(app_label)s_%(class)s_dimensions_idx",
            ),
        ]
