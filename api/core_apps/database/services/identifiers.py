# api/core_apps/database/services/identifiers.py
from __future__ import annotations

import re
from collections.abc import Iterable

IDENTIFIER_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def normalize_identifier(value: str | None, *, default: str = "public") -> str:
    normalized = str(value or default).strip()

    if not IDENTIFIER_RE.fullmatch(normalized):
        raise ValueError(f"Invalid Postgres identifier: {value!r}")

    return normalized


def normalize_identifiers(values: Iterable[str | None]) -> tuple[str, ...]:
    normalized: list[str] = []

    for value in values:
        identifier = normalize_identifier(value)
        if identifier not in normalized:
            normalized.append(identifier)

    return tuple(normalized)
