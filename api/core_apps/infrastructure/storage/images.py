# api/core_apps/infrastructure/storage/images.py
from __future__ import annotations

from PIL import Image

from core_apps.infrastructure.storage.services import MediaStorageService
from core_apps.infrastructure.storage.types import (
    PersistUploadOptions,
    StoredMediaDescriptor,
)
from core_apps.infrastructure.storage.validators import validate_image_upload


class ImageIngestService:
    def __init__(self, *, storage: MediaStorageService | None = None) -> None:
        self.storage = storage or MediaStorageService()

    def persist_image(
        self, uploaded_file, *, folder: str, filename: str | None = None
    ) -> StoredMediaDescriptor:
        validate_image_upload(uploaded_file)
        width, height = self.get_image_dimensions(uploaded_file)
        descriptor = self.storage.persist_upload(
            uploaded_file,
            PersistUploadOptions(folder=folder, filename=filename),
        )
        return StoredMediaDescriptor(
            **{
                **descriptor.as_dict(),
                "width": width,
                "height": height,
            }
        )

    def get_image_dimensions(self, uploaded_file) -> tuple[int | None, int | None]:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)

        try:
            with Image.open(uploaded_file) as image:
                width, height = image.size
                return int(width), int(height)
        finally:
            if hasattr(uploaded_file, "seek"):
                uploaded_file.seek(0)
