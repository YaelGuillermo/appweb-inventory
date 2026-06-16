# api/database/services/postgres_admin.py
from collections.abc import Iterator
from contextlib import contextmanager

import psycopg
from psycopg import Connection, sql

from .config import PostgresDatabaseConfig
from .identifiers import normalize_identifiers


@contextmanager
def admin_connection(config: PostgresDatabaseConfig) -> Iterator[Connection]:
    connection = psycopg.connect(**config.admin_connection_kwargs)
    connection.autocommit = True
    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def target_connection(config: PostgresDatabaseConfig) -> Iterator[Connection]:
    connection = psycopg.connect(**config.target_connection_kwargs)
    connection.autocommit = True
    try:
        yield connection
    finally:
        connection.close()


def database_exists(config: PostgresDatabaseConfig) -> bool:
    with admin_connection(config) as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s LIMIT 1",
            (config.name,),
        )
        return cursor.fetchone() is not None


def terminate_database_connections(config: PostgresDatabaseConfig) -> None:
    with admin_connection(config) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s
                  AND pid <> pg_backend_pid()
                """,
            (config.name,),
        )


def create_database_if_missing(config: PostgresDatabaseConfig) -> bool:
    with admin_connection(config) as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s LIMIT 1",
            (config.name,),
        )
        if cursor.fetchone() is not None:
            return False

        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(config.name))
        )
        return True


def drop_database_if_exists(config: PostgresDatabaseConfig) -> bool:
    terminate_database_connections(config)

    with admin_connection(config) as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s LIMIT 1",
            (config.name,),
        )
        if cursor.fetchone() is None:
            return False

        cursor.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(config.name)))
        return True


def ensure_database_schemas(
    config: PostgresDatabaseConfig,
    schemas: tuple[str, ...] | list[str] | None = None,
) -> tuple[str, ...]:
    target_schemas = normalize_identifiers(tuple(schemas or config.application_schemas))

    with target_connection(config) as connection, connection.cursor() as cursor:
        for schema in target_schemas:
            cursor.execute(
                sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema))
            )

    return target_schemas


def reset_database_schemas(
    config: PostgresDatabaseConfig,
    schemas: tuple[str, ...] | list[str] | None = None,
    *,
    include_public: bool = False,
) -> tuple[str, ...]:
    target_schemas = tuple(
        schema
        for schema in normalize_identifiers(
            tuple(schemas or config.application_schemas)
        )
        if include_public or schema != "public"
    )

    if not target_schemas:
        return tuple()

    with target_connection(config) as connection, connection.cursor() as cursor:
        for schema in target_schemas:
            cursor.execute(
                sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(
                    sql.Identifier(schema)
                )
            )
            cursor.execute(
                sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema))
            )
            if schema == "public":
                cursor.execute("GRANT ALL ON SCHEMA public TO public")

    return target_schemas
