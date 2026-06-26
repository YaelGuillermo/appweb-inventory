# api/core_apps/infrastructure/sql_assets/registry.py
from __future__ import annotations

from django.db import connection

from core_apps.database.services.identifiers import normalize_identifier

REGISTRY_TABLE_NAME = "sql_assets_registry"


def quote_identifier(identifier: str) -> str:
    return connection.ops.quote_name(normalize_identifier(identifier))


def ensure_registry_table(schema: str) -> None:
    quoted_schema = quote_identifier(schema)
    quoted_table = quote_identifier(REGISTRY_TABLE_NAME)

    with connection.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {quoted_schema}")
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {quoted_schema}.{quoted_table} (
                key text PRIMARY KEY,
                path text NOT NULL,
                kind text NOT NULL,
                checksum_sha256 text NOT NULL,
                synced_at timestamptz NOT NULL DEFAULT now()
            )
            """
        )


def find_registered_checksum(*, schema: str, key: str) -> str | None:
    quoted_schema = quote_identifier(schema)
    quoted_table = quote_identifier(REGISTRY_TABLE_NAME)

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT checksum_sha256
            FROM {quoted_schema}.{quoted_table}
            WHERE key = %s
            LIMIT 1
            """,
            [key],
        )
        row = cursor.fetchone()

    return row[0] if row else None


def upsert_registry(
    *,
    schema: str,
    key: str,
    path: str,
    kind: str,
    checksum_sha256: str,
) -> None:
    quoted_schema = quote_identifier(schema)
    quoted_table = quote_identifier(REGISTRY_TABLE_NAME)

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO {quoted_schema}.{quoted_table}
                (key, path, kind, checksum_sha256, synced_at)
            VALUES (%s, %s, %s, %s, now())
            ON CONFLICT (key)
            DO UPDATE SET
                path = EXCLUDED.path,
                kind = EXCLUDED.kind,
                checksum_sha256 = EXCLUDED.checksum_sha256,
                synced_at = now()
            """,
            [key, path, kind, checksum_sha256],
        )
