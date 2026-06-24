# api/core_apps/infrastructure/sql_assets/manifest.py
from core_apps.infrastructure.sql_assets.types import SqlAssetDefinition

SQL_ASSETS_MANIFEST: list[SqlAssetDefinition] = [
    # Example:
    # SqlAssetDefinition(
    #     key="users.live_programs_count",
    #     kind="function",
    #     path="core_apps/accounts/sql/functions/users_live_programs_count.sql",
    #     schema="public",
    #     name="users_live_programs_count",
    #     order=100,
    # ),
    # SqlAssetDefinition(
    #     key="programs.idx_programs_user_id_live",
    #     kind="index",
    #     path="core_apps/projects/sql/indexes/idx_programs_user_id_live.sql",
    #     schema="public",
    #     name="idx_programs_user_id_live",
    #     order=200,
    #     transactional=False,
    # ),
]
