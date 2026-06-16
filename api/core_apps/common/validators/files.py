# api/core_apps/common/validators/files.py
import re
from pathlib import PurePath

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core_apps.common.constants import (
    FILE_CHECKSUM_SHA256_LENGTH,
    FILE_EXTENSION_MAX_LENGTH,
)

SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")
FILE_EXTENSION_RE = re.compile(r"^[a-zA-Z0-9]+$")


def validate_file_extension(value: str) -> None:
    extension = str(value or "").strip().lower().removeprefix(".")

    if not extension:
        raise ValidationError(_("The file extension cannot be blank."), code="blank")

    if len(extension) > FILE_EXTENSION_MAX_LENGTH:
        raise ValidationError(
            _("The file extension cannot exceed %(max_length)s characters."),
            code="max_length",
            params={"max_length": FILE_EXTENSION_MAX_LENGTH},
        )

    if not FILE_EXTENSION_RE.fullmatch(extension):
        raise ValidationError(
            _("The file extension contains unsupported characters."),
            code="invalid",
        )


def validate_sha256_checksum(value: str | None) -> None:
    if value in (None, ""):
        return

    checksum = str(value).strip()

    if len(checksum) != FILE_CHECKSUM_SHA256_LENGTH or not SHA256_RE.fullmatch(
        checksum
    ):
        raise ValidationError(
            _("Enter a valid SHA-256 checksum."),
            code="invalid_sha256",
        )


def validate_relative_storage_path(value: str) -> None:
    path = str(value or "").strip()

    if not path:
        raise ValidationError(_("The file path cannot be blank."), code="blank")

    pure_path = PurePath(path)

    if pure_path.is_absolute() or ".." in pure_path.parts:
        raise ValidationError(
            _("The file path must be a safe relative path."),
            code="unsafe_path",
        )
