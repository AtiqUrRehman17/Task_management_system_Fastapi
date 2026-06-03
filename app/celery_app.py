from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "task_management",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
)

celery_app.autodiscover_tasks(
    ["app.workers"]
)