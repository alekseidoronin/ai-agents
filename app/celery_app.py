from celery import Celery

from app.config import settings

celery = Celery(
    "ai_agents",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    task_track_started=True,
    task_acks_late=True,
)

celery.autodiscover_tasks(["app.tasks"])
