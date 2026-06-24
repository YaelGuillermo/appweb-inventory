# api/core_apps/infrastructure/storage/constants.py
STORAGE_TEMP_FOLDER = "_tmp"
STORAGE_HEALTHCHECK_FOLDER = "_healthcheck"
STORAGE_DEFAULT_IMAGE_EXTENSION = "jpg"
STORAGE_DEFAULT_IMAGE_MIME_TYPE = "image/jpeg"

MIME_EXTENSION_MAP = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/gif": "gif",
    "image/svg+xml": "svg",
}
