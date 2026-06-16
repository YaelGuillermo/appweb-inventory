# api/database/services/table_maintenance.py
from dataclasses import dataclass

from psycopg import sql

from .config import PostgresDatabaseConfig
from .identifiers import normalize_identifiers
from .postgres_admin import target_connection


@dataclass(frozen=True, slots=True)
class DatabaseTableReference:
    schema: str
    table_name: str


def list_database_tables(
    config: PostgresDatabaseConfig,
    schemas: tuple[str, ...] | list[str] | None = None,
) -> list[DatabaseTableReference]:
    target_schemas = normalize_identifiers(tuple(schemas or config.application_schemas))

    with target_connection(config) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE'
                  AND table_schema = ANY(%s)
                ORDER BY table_schema ASC, table_name ASC
                """,
            (list(target_schemas),),
        )
        return [
            DatabaseTableReference(schema=row[0], table_name=row[1])
            for row in cursor.fetchall()
        ]


def truncate_database_tables(
    config: PostgresDatabaseConfig,
    schemas: tuple[str, ...] | list[str] | None = None,
    *,
    include_migrations_table: bool = False,
) -> list[DatabaseTableReference]:
    tables = [
        table
        for table in list_database_tables(config, schemas)
        if include_migrations_table or table.table_name != "django_migrations"
    ]

    if not tables:
        return []

    table_identifiers = [
        sql.SQL("{}.{}").format(
            sql.Identifier(table.schema), sql.Identifier(table.table_name)
        )
        for table in tables
    ]

    query = sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE").format(
        sql.SQL(", ").join(table_identifiers)
    )

    with target_connection(config) as connection, connection.cursor() as cursor:
        cursor.execute(query)

    return tables
