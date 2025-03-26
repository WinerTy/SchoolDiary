from celery import Celery

from core.config import config

celery_app = Celery(
    "worker",
    broker=str(config.redis.url),
    backend=str(config.redis.url),
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

celery_app.autodiscover_tasks()
