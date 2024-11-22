import asyncio
import datetime
import json
import logging

import redis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config

from handlers import router
from storages import message_transfer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
bot = Bot(token=config.BOT_TOKEN(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


def message_format(msg_model: dict) -> str:
    return f"""<b>Сообщение от <i>{
    msg_model["sender"]
    } :</i></b>\n\n{
    msg_model["text"]
    }\n\n<i>{
    datetime.datetime.strptime(
        msg_model["created_at"], '%Y-%m-%dT%H:%M:%S.%f'
    ).strftime('%H:%M:%S %d.%m.%Y')
    }</i>"""


async def event_catcher():
    p = message_transfer.connection.pubsub()
    try:
        await p.subscribe("message_to_tg")
        while True:
            message = await p.get_message(ignore_subscribe_messages=True)
            if message is not None:
                msg_raw = json.loads(message["data"])
                output = message_format(msg_raw)
                chat_id = msg_raw["receiver"]
                await bot.send_message(chat_id, output)
    except redis.exceptions.ConnectionError:
        raise


async def main():
    dp.include_router(router)
    asyncio.create_task(event_catcher())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
