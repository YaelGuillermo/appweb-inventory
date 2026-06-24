# api/core_apps/infrastructure/sql_assets/types.py
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

SqlAssetKind = Literal[
    "extension",
    "function",
    "index",
    "materialized_view",
    "policy",
    "procedure",
    "trigger",
    "view",
    "other",
]
SqlAssetStatus = Literal["created", "updated", "unchanged", "skipped", "dry_run"]


@dataclass(frozen=True, slots=True)
class SqlAssetDefinition:
    key: str
    path: str
    kind: SqlAssetKind
    name: str | None = None
    schema: str | None = None
    enabled: bool = True
    order: int = 0
    transactional: bool = True


@dataclass(frozen=True, slots=True)
class SqlAssetSyncOptions:
    force: bool = False
    dry_run: bool = False
    include_disabled: bool = False


@dataclass(frozen=True, slots=True)
class SqlAssetSyncResult:
    key: str
    path: str
    kind: SqlAssetKind
    status: SqlAssetStatus
    checksum_sha256: str

    def as_dict(self) -> dict:
        return asdict(self)
