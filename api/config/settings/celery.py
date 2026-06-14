# api/config/settings/celery.py
from kombu import Queue
from config.env import env

REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default=REDIS_URL)
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default=REDIS_URL.replace("/0", "/1"))

CELERY_TIMEZONE = env("DJANGO_TIME_ZONE", default="UTC")
CELERY_TASK_ALWAYS_EAGER = env.bool("CELERY_TASK_ALWAYS_EAGER", default=False)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_DEFAULT_QUEUE = env("CELERY_TASK_DEFAULT_QUEUE", default="default")
CELERY_TASK_DEFAULT_EXCHANGE = env("CELERY_TASK_DEFAULT_EXCHANGE", default="default")
CELERY_TASK_DEFAULT_ROUTING_KEY = env("CELERY_TASK_DEFAULT_ROUTING_KEY", default="default")

CELERY_TASK_QUEUE_NAMES = [
    queue_name.strip()
    for queue_name in env("CELERY_TASK_QUEUE_NAMES", default="default,heavy").split(",")
    if queue_name.strip()
]

CELERY_TASK_QUEUES = tuple(Queue(queue_name) for queue_name in CELERY_TASK_QUEUE_NAMES)

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_FLOWER_USER = env("CELERY_FLOWER_USER", default="admin")
CELERY_FLOWER_PASSWORD = env("CELERY_FLOWER_PASSWORD", default="flower")