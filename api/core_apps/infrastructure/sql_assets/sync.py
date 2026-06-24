# api/core_apps/infrastructure/sql_assets/sync.py
from __future__ import annotations

from importlib import import_module

from django.conf import settings
from django.db import connection, transaction

from core_apps.infrastructure.sql_assets.reader import hash_sql, read_sql_file
from core_apps.infrastructure.sql_assets.registry import (
    ensure_registry_table,
    find_registered_checksum,
    upsert_registry,
)
from core_apps.infrastructure.sql_assets.types import (
    SqlAssetDefinition,
    SqlAssetSyncOptions,
    SqlAssetSyncResult,
)


def sort_assets(assets: list[SqlAssetDefinition]) -> list[SqlAssetDefinition]:
    return sorted(assets, key=lambda asset: (asset.order, asset.key))


def load_manifest(module_path: str | None = None) -> list[SqlAssetDefinition]:
    manifest_module_path = module_path or getattr(
        settings,
        "SQL_ASSETS_MANIFEST_MODULE",
        "core_apps.infrastructure.sql_assets.manifest",
    )
    module = import_module(manifest_module_path)
    assets = getattr(module, "SQL_ASSETS_MANIFEST", None)

    if assets is None:
        assets = getattr(module, "default", [])

    return list(assets or [])


def execute_sql(sql: str) -> None:
    with connection.cursor() as cursor:
        cursor.execute(sql)


def sync_sql_assets(
    assets: list[SqlAssetDefinition] | None = None,
    options: SqlAssetSyncOptions | None = None,
    *,
    manifest_module: str | None = None,
    registry_schema: str | None = None,
) -> list[SqlAssetSyncResult]:
    options = options or SqlAssetSyncOptions()
    sql_assets = list(assets if assets is not None else load_manifest(manifest_module))
    schema = registry_schema or getattr(settings, "DB_SCHEMA", "public")
    results: list[SqlAssetSyncResult] = []

    ensure_registry_table(schema)

    for asset in sort_assets(sql_assets):
        sql = read_sql_file(asset.path)
        checksum_sha256 = hash_sql(sql)

        if asset.enabled is False and not options.include_disabled:
            results.append(
                SqlAssetSyncResult(
                    key=asset.key,
                    path=asset.path,
                    kind=asset.kind,
                    status="skipped",
                    checksum_sha256=checksum_sha256,
                )
            )
            continue

        registered_checksum = find_registered_checksum(schema=schema, key=asset.key)
        should_run = options.force or registered_checksum != checksum_sha256

        if not should_run:
            results.append(
                SqlAssetSyncResult(
                    key=asset.key,
                    path=asset.path,
                    kind=asset.kind,
                    status="unchanged",
                    checksum_sha256=checksum_sha256,
                )
            )
            continue

        if options.dry_run:
            results.append(
                SqlAssetSyncResult(
                    key=asset.key,
                    path=asset.path,
                    kind=asset.kind,
                    status="dry_run",
                    checksum_sha256=checksum_sha256,
                )
            )
            continue

        if asset.transactional:
            with transaction.atomic():
                execute_sql(sql)
                upsert_registry(
                    schema=schema,
                    key=asset.key,
                    path=asset.path,
                    kind=asset.kind,
                    checksum_sha256=checksum_sha256,
                )
        else:
            if connection.in_atomic_block:
                raise RuntimeError(
                    f"SQL asset {asset.key!r} is marked as non-transactional but an atomic block is active."
                )
            execute_sql(sql)
            upsert_registry(
                schema=schema,
                key=asset.key,
                path=asset.path,
                kind=asset.kind,
                checksum_sha256=checksum_sha256,
            )

        results.append(
            SqlAssetSyncResult(
                key=asset.key,
                path=asset.path,
                kind=asset.kind,
                status="updated" if registered_checksum else "created",
                checksum_sha256=checksum_sha256,
            )
        )

    return results
