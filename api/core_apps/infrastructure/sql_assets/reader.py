# api/core_apps/infrastructure/sql_assets/reader.py
from __future__ import annotations

import hashlib
from pathlib import Path

from django.conf import settings


def normalize_sql_asset_path(path: str) -> str:
    return str(path or "").replace("\\", "/").lstrip("/")


def resolve_sql_asset_path(path: str) -> Path:
    candidate_path = Path(path)
    if candidate_path.is_absolute():
        return candidate_path

    normalized = normalize_sql_asset_path(path)
    base_dir = Path(settings.BASE_DIR)
    apps_dir = Path(getattr(settings, "APPS_DIR", base_dir / "core_apps"))

    candidates = [
        base_dir / normalized,
        apps_dir / normalized,
        base_dir / "sql" / normalized,
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(f"SQL asset not found: {path}")


def read_sql_file(path: str) -> str:
    sql = resolve_sql_asset_path(path).read_text(encoding="utf-8")
    return sql.strip()


def hash_sql(sql: str) -> str:
    return hashlib.sha256(sql.encode("utf-8")).hexdigest()
