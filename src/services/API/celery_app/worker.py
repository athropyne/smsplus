import asyncio

from celery import Celery

from core import config
from core.storages import message_transfer

celery = Celery(__name__, broker=config.CELERY_REDIS_BROKER_DSN(), backend=config.CELERY_REDIS_BROKER_DSN())


@celery.task
def notify(tg_id: int, message: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(message_transfer.connection.publish("message", message))
