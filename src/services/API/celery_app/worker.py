import asyncio

from celery import Celery

from core import config
from core.storages import message_transfer

celery = Celery(__name__,
                broker=config.settings.CELERY_REDIS_BROKER,
                backend=config.settings.CELERY_REDIS_BROKER)


@celery.task
def notify(message: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(message_transfer.connection.publish("message_to_tg", message))
