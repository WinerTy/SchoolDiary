from celery import Celery

from core.config import config

celery_app = Celery(
    "worker",
    broker=str(config.redis.url),
    backend=str(config.redis.url),
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

celery_app.autodiscover_tasks()
