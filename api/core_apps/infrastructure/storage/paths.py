# api/core_apps/infrastructure/storage/paths.py
from __future__ import annotations

from pathlib import PurePosixPath
from urllib.parse import urljoin


def sanitize_slashes(value: str | None) -> str:
    return str(value or "").strip().replace("\\", "/")


def normalize_relative_media_path(value: str | None) -> str:
    raw_value = sanitize_slashes(value)
    normalized = str(PurePosixPath(raw_value)).strip("/")

    if normalized in ("", "."):
        return ""

    parts = PurePosixPath(normalized).parts
    if ".." in parts:
        raise ValueError(f"Unsafe media path: {value!r}")

    return normalized


def normalize_media_public_path(value: str | None) -> str:
    normalized = sanitize_slashes(value or "media").strip("/")
    return f"/{normalized or 'media'}"


def build_media_relative_path(folder: str | None, filename: str) -> str:
    safe_folder = normalize_relative_media_path(folder)
    safe_filename = normalize_relative_media_path(filename)

    if not safe_filename:
        raise ValueError("Invalid media filename.")

    return f"{safe_folder}/{safe_filename}" if safe_folder else safe_filename


def join_public_media_path(public_path: str | None, relative_path: str) -> str:
    safe_public_path = normalize_media_public_path(public_path)
    safe_relative_path = normalize_relative_media_path(relative_path)
    return f"{safe_public_path}/{safe_relative_path}"


def join_public_media_url(public_url: str | None, relative_path: str) -> str | None:
    if not public_url:
        return None

    safe_relative_path = normalize_relative_media_path(relative_path)
    return urljoin(f"{public_url.rstrip('/')}/", safe_relative_path)
