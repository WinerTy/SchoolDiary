from celery import Celery

from core.config import config

celery_app = Celery(
    "worker",
    broker=str(config.redis.url),
    backend=str(config.redis.url),
)

celery_app.conf.update(,

celery_app.autodiscover_tasks()
