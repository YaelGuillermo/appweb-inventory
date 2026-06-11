# api/config/env.py
import environ
import os
import sys
from pathlib import Path

env = environ.Env()

# Path configuration
BASE_DIR = Path(__file__).resolve().parent.parent
ENVS_DIR = BASE_DIR / "config" / "env"

# Constants
VALID_ENVS = ("local", "production", "staging", "test")
DEFAULT_ENV = "local"
SETTINGS_BASE = "config.django"


def validate_settings_module(module_path):
    """Valida que el módulo de settings tenga el formato correcto."""
    if not module_path:
        return False

    parts = module_path.split(".")
    return (
        len(parts) == 3
        and parts[0] == "config"
        and parts[1] == "django"
        and parts[2] in VALID_ENVS
    )


# 1. Get and validate DJANGO_SETTINGS_MODULE
settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")

# 2. Set default if not provided or invalid
if not validate_settings_module(settings_module):
    if settings_module:
        sys.stderr.write(
            f"Error: Invalid DJANGO_SETTINGS_MODULE='{settings_module}'. "
            f"Expected format: '{SETTINGS_BASE}.<env>' where <env> is one of {VALID_ENVS}\n"
        )

    settings_module = f"{SETTINGS_BASE}.{DEFAULT_ENV}"
    os.environ["DJANGO_SETTINGS_MODULE"] = settings_module
    sys.stderr.write(f"Using default settings module: {settings_module}\n")

# 3. Extract environment name
env_name = settings_module.split(".")[-1]

# 4. Load environment-specific variables
env_file = ENVS_DIR / f".env.{env_name}"
if env_file.exists():
    env.read_env(env_file)
    print(f"Loaded environment variables from {env_file}")
elif env_name != "test":
    sys.stderr.write(f"Warning: Environment file not found at {env_file}\n")

# Ensure consistency
if os.environ["DJANGO_SETTINGS_MODULE"] != settings_module:
    os.environ["DJANGO_SETTINGS_MODULE"] = settings_module