from __future__ import annotations


def normalize_human_name(value: str | None) -> str:
    return " ".join(str(value or "").split())
