# api/config/settings/channels.py
from config.env import env

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env("CHANNEL_REDIS_URL", default="redis://localhost:6379/2")],
        },
    },
}
