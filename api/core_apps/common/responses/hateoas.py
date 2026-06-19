from __future__ import annotations

from typing import Literal
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]


def build_link(href: str, method: HttpMethod = "GET", title: str | None = None) -> dict:
    link = {"href": href, "method": method}

    if title:
        link["title"] = title

    return link


def strip_query(path: str) -> str:
    return path.split("?", 1)[0]


def build_url_with_query(path: str, query: dict[str, object]) -> str:
    split = urlsplit(path)
    current_query = dict(parse_qsl(split.query, keep_blank_values=True))

    for key, value in query.items():
        if value is None:
            current_query.pop(key, None)
        else:
            current_query[key] = str(value)

    return urlunsplit(
        (
            split.scheme,
            split.netloc,
            split.path,
            urlencode(current_query),
            split.fragment,
        )
    )


def build_page_url(path: str, page: int, page_size: int) -> str:
    return build_url_with_query(path, {"page": page, "page_size": page_size})


def build_base_links(path: str) -> dict:
    return {"self": build_link(path, "GET")}


def build_collection_links(
    *,
    path: str,
    pagination: dict | None = None,
    allow_create: bool = False,
) -> dict:
    links = build_base_links(path)

    if allow_create:
        links["create"] = build_link(strip_query(path), "POST")

    page_links = (pagination or {}).get("links") or {}
    for key in ("first", "last", "previous", "next"):
        href = page_links.get(key)
        if href:
            links[key] = build_link(href, "GET")

    return links


def build_detail_links(
    *,
    path: str,
    collection_path: str | None = None,
    allow_update: bool = True,
    allow_delete: bool = True,
) -> dict:
    links = build_base_links(path)

    if collection_path:
        links["collection"] = build_link(collection_path, "GET")

    if allow_update:
        links["update"] = build_link(path, "PATCH")

    if allow_delete:
        links["delete"] = build_link(path, "DELETE")

    return links


def merge_links(*sources: dict | None) -> dict:
    merged: dict = {}

    for source in sources:
        if source:
            merged.update(source)

    return merged
