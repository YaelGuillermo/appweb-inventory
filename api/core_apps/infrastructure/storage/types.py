# api/core_apps/infrastructure/storage/types.py
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

MediaStorageDriver = Literal["local", "s3", "custom"]
MediaVisibility = Literal["public", "private"]


@dataclass(frozen=True, slots=True)
class PersistUploadOptions:
    folder: str
    filename: str | None = None
    visibility: MediaVisibility = "public"


@dataclass(frozen=True, slots=True)
class StoredMediaDescriptor:
    driver: MediaStorageDriver
    key: str
    relative_path: str
    public_path: str
    original_name: str
    mime_type: str
    size_bytes: int
    extension: str
    checksum_sha256: str | None = None
    public_url: str | None = None
    width: int | None = None
    height: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}
