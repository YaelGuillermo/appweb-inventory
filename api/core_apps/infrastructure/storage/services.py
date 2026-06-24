# api/core_apps/infrastructure/storage/services.py
from __future__ import annotations

import hashlib
from pathlib import PurePosixPath
from uuid import uuid4

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from core_apps.infrastructure.storage.constants import STORAGE_HEALTHCHECK_FOLDER
from core_apps.infrastructure.storage.paths import (
    build_media_relative_path,
    join_public_media_path,
    join_public_media_url,
    normalize_relative_media_path,
)
from core_apps.infrastructure.storage.types import (
    PersistUploadOptions,
    StoredMediaDescriptor,
)
from core_apps.infrastructure.storage.validators import (
    resolve_upload_extension,
    validate_upload_size,
)


class MediaStorageService:
    @property
    def driver(self) -> str:
        backend_path = default_storage.__class__.__module__.lower()
        backend_name = default_storage.__class__.__name__.lower()

        if "s3" in backend_path or "boto" in backend_path or "s3" in backend_name:
            return "s3"
        if "filesystem" in backend_path or "filesystem" in backend_name:
            return "local"
        return "custom"

    @property
    def public_path(self) -> str:
        return str(getattr(settings, "MEDIA_URL", "/media/"))

    def get_runtime_details(self) -> dict:
        details = {
            "driver": self.driver,
            "storage_backend": f"{default_storage.__class__.__module__}.{default_storage.__class__.__name__}",
            "public_path": self.public_path,
            "public_url": getattr(settings, "MEDIA_STORAGE_PUBLIC_URL", None) or None,
        }

        if self.driver == "local":
            details["local_root_dir"] = str(getattr(settings, "MEDIA_ROOT", ""))
        elif self.driver == "s3":
            details["bucket_name"] = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)
            details["region"] = getattr(settings, "AWS_S3_REGION_NAME", None)
            details["custom_domain"] = getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)

        return details

    def to_public_path(self, relative_path: str) -> str:
        try:
            return default_storage.url(normalize_relative_media_path(relative_path))
        except Exception:
            return join_public_media_path(self.public_path, relative_path)

    def to_public_url(self, relative_path: str) -> str | None:
        public_url = getattr(settings, "MEDIA_STORAGE_PUBLIC_URL", "") or ""
        if public_url:
            return join_public_media_url(public_url, relative_path)

        public_path = self.to_public_path(relative_path)
        if public_path.startswith("http://") or public_path.startswith("https://"):
            return public_path
        return None

    def persist_upload(
        self, uploaded_file, options: PersistUploadOptions
    ) -> StoredMediaDescriptor:
        validate_upload_size(uploaded_file)

        folder = normalize_relative_media_path(options.folder)
        extension = resolve_upload_extension(uploaded_file)
        filename = options.filename or f"{uuid4()}.{extension}"
        relative_path = build_media_relative_path(folder, filename)
        checksum_sha256 = self.compute_sha256(uploaded_file)
        saved_path = default_storage.save(relative_path, uploaded_file)

        return StoredMediaDescriptor(
            driver=self.driver,
            key=saved_path,
            relative_path=saved_path,
            public_path=self.to_public_path(saved_path),
            public_url=self.to_public_url(saved_path),
            original_name=str(getattr(uploaded_file, "name", filename) or filename),
            mime_type=str(
                getattr(uploaded_file, "content_type", "application/octet-stream")
            ),
            size_bytes=int(getattr(uploaded_file, "size", 0) or 0),
            extension=extension,
            checksum_sha256=checksum_sha256,
        )

    def duplicate_relative_path(
        self, relative_path: str, target_folder: str | None = None
    ) -> str:
        source_relative_path = normalize_relative_media_path(relative_path)
        fallback_folder = str(PurePosixPath(source_relative_path).parent)
        folder = normalize_relative_media_path(
            target_folder
            if target_folder is not None
            else ("" if fallback_folder == "." else fallback_folder)
        )
        extension = PurePosixPath(source_relative_path).suffix.lower()
        filename = f"{uuid4()}{extension}"
        duplicated_relative_path = build_media_relative_path(folder, filename)

        with default_storage.open(source_relative_path, "rb") as source_file:
            default_storage.save(duplicated_relative_path, source_file)

        return duplicated_relative_path

    def delete_many(self, relative_paths: list[str]) -> None:
        for relative_path in filter(None, relative_paths or []):
            safe_path = normalize_relative_media_path(relative_path)
            if default_storage.exists(safe_path):
                default_storage.delete(safe_path)

    def assert_healthy(self) -> None:
        relative_path = build_media_relative_path(
            STORAGE_HEALTHCHECK_FOLDER,
            f".storage-{uuid4()}.tmp",
        )
        saved_path = default_storage.save(relative_path, ContentFile(b"ok"))
        default_storage.delete(saved_path)

    def compute_sha256(self, uploaded_file) -> str | None:
        hasher = hashlib.sha256()
        has_content = False

        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)

        if hasattr(uploaded_file, "chunks"):
            for chunk in uploaded_file.chunks():
                hasher.update(chunk)
                has_content = True
        else:
            data = uploaded_file.read()
            hasher.update(data)
            has_content = bool(data)

        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)

        return hasher.hexdigest() if has_content else None
