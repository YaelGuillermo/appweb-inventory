# api/database/services/config.py
from dataclasses import dataclass
from typing import Any

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .identifiers import normalize_identifier, normalize_identifiers


@dataclass(frozen=True, slots=True)
class PostgresDatabaseConfig:
    host: str
    port: int
    name: str
    username: str
    password: str
    schema: str
    application_schemas: tuple[str, ...]
    admin_database: str
    sslmode: str
    connect_timeout: int

    @property
    def target_connection_kwargs(self) -> dict[str, Any]:
        return self.connection_kwargs(database_name=self.name)

    @property
    def admin_connection_kwargs(self) -> dict[str, Any]:
        return self.connection_kwargs(database_name=self.admin_database)

    def connection_kwargs(self, *, database_name: str) -> dict[str, Any]:
        return {
            "host": self.host,
            "port": self.port,
            "dbname": database_name,
            "user": self.username,
            "password": self.password,
            "sslmode": self.sslmode,
            "connect_timeout": self.connect_timeout,
        }


def get_postgres_config(alias: str = "default") -> PostgresDatabaseConfig:
    databases = getattr(settings, "DATABASES", {})
    database = databases.get(alias)

    if not database:
        raise ImproperlyConfigured(f'Database alias "{alias}" is not configured.')

    engine = database.get("ENGINE", "")
    if "postgresql" not in engine:
        raise ImproperlyConfigured(
            f'Database alias "{alias}" must use PostgreSQL. Current ENGINE={engine!r}.'
        )

    options = database.get("OPTIONS", {}) or {}
    schema = normalize_identifier(getattr(settings, "DB_SCHEMA", "public"))
    application_schemas = normalize_identifiers(
        tuple(getattr(settings, "DB_APPLICATION_SCHEMAS", (schema,)))
    )

    return PostgresDatabaseConfig(
        host=str(database.get("HOST") or "localhost"),
        port=int(database.get("PORT") or 5432),
        name=str(database.get("NAME") or ""),
        username=str(database.get("USER") or ""),
        password=str(database.get("PASSWORD") or ""),
        schema=schema,
        application_schemas=application_schemas,
        admin_database=str(getattr(settings, "DB_ADMIN_DATABASE", "postgres")),
        sslmode=str(options.get("sslmode") or getattr(settings, "DB_SSLMODE", "prefer")),
        connect_timeout=int(options.get("connect_timeout") or getattr(settings, "DB_CONNECT_TIMEOUT", 10)),
    )
