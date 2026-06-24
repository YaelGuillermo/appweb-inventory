# api/tests/unit/infrastructure/test_media_paths.py
import pytest

from core_apps.infrastructure.storage.paths import (
    build_media_relative_path,
    normalize_relative_media_path,
)


def test_normalize_relative_media_path_rejects_parent_traversal():
    with pytest.raises(ValueError):
        normalize_relative_media_path("../unsafe/file.png")


def test_build_media_relative_path_uses_safe_posix_paths():
    assert (
        build_media_relative_path("avatars/users", "image.png")
        == "avatars/users/image.png"
    )
