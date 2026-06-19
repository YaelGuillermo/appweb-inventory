from __future__ import annotations


def normalize_file_extension(value: str | None) -> str:
    return str(value or "").strip().lower().removeprefix(".")


def normalize_mime_type(value: str | None) -> str:
    return str(value or "").strip().lower()


def normalize_original_name(value: str | None) -> str:
    return str(value or "").strip()


def normalize_storage_path(value: str | None) -> str:
    return str(value or "").strip()


def normalize_sha256_checksum(value: str | None) -> str | None:
    normalized = str(value or "").strip().lower()
    return normalized or None
