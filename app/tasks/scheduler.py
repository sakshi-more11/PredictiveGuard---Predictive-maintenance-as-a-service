from celery import Celery
from celery.schedules import crontab
from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

# Configure periodic tasks
celery_app.conf.beat_schedule = {
    'check-alerts-every-5-minutes': {
        'task': 'app.tasks.worker_tasks.check_alerts',
        'schedule': 300.0,  # 5 minutes
    },
}

logger.info("Celery Beat schedule configured")