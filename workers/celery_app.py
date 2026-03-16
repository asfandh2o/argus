import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from celery import Celery
from celery.schedules import crontab
from core.config import settings

celery_app = Celery(
    "argus",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
)

celery_app.conf.beat_schedule = {
    "sync-employees-from-hera": {
        "task": "workers.tasks.sync_employees",
        "schedule": crontab(minute="*/15"),
    },
    "collect-and-score": {
        "task": "workers.tasks.collect_and_score",
        "schedule": crontab(minute=f"*/{settings.COLLECTION_INTERVAL_MINUTES}"),
    },
}

if __name__ == "__main__":
    celery_app.start()
