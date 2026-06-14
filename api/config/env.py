# api/config/env.py
import os
import sys
from pathlib import Path

import environ

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
ENVS_DIR = BASE_DIR / "env"

VALID_ENVS = ("local", "production", "staging", "test")
DEFAULT_ENV = "local"
SETTINGS_BASE = "config.django"


def validate_settings_module(module_path: str | None) -> bool:
    if not module_path:
        return False

    parts = module_path.split(".")

    return (
        len(parts) == 3
        and parts[0] == "config"
        and parts[1] == "django"
        and parts[2] in VALID_ENVS
    )


settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")

if not validate_settings_module(settings_module):
    if settings_module:
        sys.stderr.write(
            f"Invalid DJANGO_SETTINGS_MODULE='{settings_module}'. "
            f"Expected '{SETTINGS_BASE}.<env>' where <env> is one of {VALID_ENVS}.\n"
        )

    settings_module = f"{SETTINGS_BASE}.{DEFAULT_ENV}"
    os.environ["DJANGO_SETTINGS_MODULE"] = settings_module
    sys.stderr.write(f"Using default settings module: {settings_module}\n")

env_name = settings_module.split(".")[-1]
env_file = ENVS_DIR / f".env.{env_name}"

if env_file.exists():
    env.read_env(str(env_file))
elif env_name != "test":
    sys.stderr.write(f"Warning: Environment file not found at {env_file}\n")