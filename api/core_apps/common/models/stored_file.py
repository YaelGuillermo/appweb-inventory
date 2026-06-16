# api/core_apps/common/models/stored_file.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.common.constants import (
    FILE_CHECKSUM_SHA256_LENGTH,
    FILE_EXTENSION_MAX_LENGTH,
    FILE_MIME_TYPE_MAX_LENGTH,
    FILE_ORIGINAL_NAME_MAX_LENGTH,
    FILE_PATH_MAX_LENGTH,
)
from core_apps.common.validators import (
    validate_file_extension,
    validate_relative_storage_path,
    validate_sha256_checksum,
)

from .base import BaseModel


class StoredFileModel(BaseModel):
    """
    Abstract model for stored file metadata.

    This model stores metadata only. The binary file should live in your storage
    backend: local media, S3, Cloudflare R2, or another service.
    """

    path = models.CharField(
        max_length=FILE_PATH_MAX_LENGTH,
        verbose_name=_("Path"),
        help_text=_("Safe relative storage path."),
        validators=[validate_relative_storage_path],
    )
    original_name = models.CharField(
        max_length=FILE_ORIGINAL_NAME_MAX_LENGTH,
        verbose_name=_("Original name"),
        help_text=_("Original uploaded file name."),
    )
    mime_type = models.CharField(
        max_length=FILE_MIME_TYPE_MAX_LENGTH,
        verbose_name=_("MIME type"),
        help_text=_("MIME type, such as image/png or application/pdf."),
    )
    size_bytes = models.PositiveBigIntegerField(
        verbose_name=_("Size in bytes"),
        help_text=_("File size in bytes."),
    )
    extension = models.CharField(
        max_length=FILE_EXTENSION_MAX_LENGTH,
        verbose_name=_("Extension"),
        help_text=_("Normalized extension without leading dot."),
        validators=[validate_file_extension],
    )
    checksum_sha256 = models.CharField(
        max_length=FILE_CHECKSUM_SHA256_LENGTH,
        null=True,
        blank=True,
        default=None,
        verbose_name=_("SHA-256 checksum"),
        help_text=_("Optional SHA-256 checksum for integrity checks."),
        validators=[validate_sha256_checksum],
    )

    class Meta(BaseModel.Meta):
        abstract = True
        verbose_name = _("Stored file")
        verbose_name_plural = _("Stored files")
        indexes = [
            *BaseModel.Meta.indexes,
            models.Index(
                fields=["path"],
                name="%(app_label)s_%(class)s_path_idx",
            ),
            models.Index(
                fields=["checksum_sha256"],
                name="%(app_label)s_%(class)s_sha256_idx",
            ),
        ]

    def clean(self) -> None:
        super().clean()

        if isinstance(self.path, str):
            self.path = self.path.strip()

        if isinstance(self.original_name, str):
            self.original_name = self.original_name.strip()

        if isinstance(self.mime_type, str):
            self.mime_type = self.mime_type.strip().lower()

        if isinstance(self.extension, str):
            self.extension = self.extension.strip().lower().removeprefix(".")
