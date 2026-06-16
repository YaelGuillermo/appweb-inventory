# api/localization/services/paths.py
from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def working_directory(path: Path) -> Iterator[None]:
    previous_path = Path.cwd()
    os.chdir(path)

    try:
        yield
    finally:
        os.chdir(previous_path)
