# api/core_apps/infrastructure/storage/validators.py
from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core_apps.infrastructure.storage.constants import (
    MIME_EXTENSION_MAP,
    STORAGE_DEFAULT_IMAGE_EXTENSION,
    STORAGE_DEFAULT_IMAGE_MIME_TYPE,
)


def normalize_file_type(value: str | None) -> str:
    return str(value or "").strip().lower().removeprefix(".")


def extension_from_mime_type(mime_type: str | None) -> str:
    if not mime_type:
        return STORAGE_DEFAULT_IMAGE_EXTENSION
    return MIME_EXTENSION_MAP.get(mime_type.lower(), STORAGE_DEFAULT_IMAGE_EXTENSION)


def mime_type_from_extension(extension: str | None) -> str:
    normalized = normalize_file_type(extension)
    for mime_type, candidate_extension in MIME_EXTENSION_MAP.items():
        if candidate_extension == normalized:
            return mime_type
    return STORAGE_DEFAULT_IMAGE_MIME_TYPE


def resolve_upload_extension(uploaded_file) -> str:
    original_extension = Path(getattr(uploaded_file, "name", "")).suffix
    normalized_extension = normalize_file_type(original_extension)
    return normalized_extension or extension_from_mime_type(
        getattr(uploaded_file, "content_type", None)
    )


def validate_upload_size(uploaded_file, *, max_size_bytes: int | None = None) -> None:
    max_size = (
        int(max_size_bytes)
        if max_size_bytes is not None
        else int(getattr(settings, "MEDIA_FILE_MAX_SIZE_BYTES", 0))
    )
    size = int(getattr(uploaded_file, "size", 0) or 0)

    if max_size > 0 and size > max_size:
        raise ValidationError(
            _("File exceeds the maximum size of %(max_size)s bytes."),
            code="file_too_large",
            params={"max_size": max_size},
        )


def is_allowed_image_file(
    uploaded_file, allowed_mime_types: list[str] | None = None
) -> bool:
    mime_type = str(getattr(uploaded_file, "content_type", "") or "").lower()

    if not mime_type.startswith("image/"):
        return False

    allowed = allowed_mime_types
    if allowed is None:
        allowed = list(getattr(settings, "MEDIA_IMAGE_ALLOWED_MIME_TYPES", []))

    if not allowed:
        return True

    extension = resolve_upload_extension(uploaded_file)
    candidates = {mime_type, extension, f"image/{extension}"}
    if extension == "jpg":
        candidates.add("jpeg")
        candidates.add("image/jpeg")

    return any(normalize_file_type(item) in candidates for item in allowed)


def validate_image_upload(uploaded_file) -> None:
    validate_upload_size(uploaded_file)

    if not is_allowed_image_file(uploaded_file):
        raise ValidationError(
            _("Unsupported image type."),
            code="invalid_image_type",
        )
