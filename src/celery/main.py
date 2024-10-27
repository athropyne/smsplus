from celery import Celery

from src.core import config

app = Celery("notificator", config.CELERY_REDIS_BROKER_URI())


@app.task
def send_message_for_offline_user(message: str):
    ...
