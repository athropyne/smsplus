#!/usr/bin/env python

import asyncio
import json
import platform
import signal
import sys

import websockets.exceptions
from redis.asyncio.client import PubSub
from websockets.asyncio.server import serve, ServerConnection

from core import config
from core.config import logger
from core.storage import online_user_storage, online
from dto import Event, EventTypes
from exc import SecurityServiceConnectionError, InvalidToken
from service import add_to_storage, check_token
from signals import Signals, Rejects


async def relay(socket: ServerConnection, user_id: int):
    async with online_user_storage as connection:
        p: PubSub = connection.pubsub()
        await p.subscribe(f"message_to_{user_id}")
        while True:
            message = await p.get_message(ignore_subscribe_messages=True)
            if message:
                asyncio.create_task(socket.send(
                    Event(type=EventTypes.MESSAGE,
                          data=json.loads(message["data"]
                                          .decode()))
                    .model_dump_json(),
                    text=True))
            await socket.ping()
            await asyncio.sleep(1)


async def handler(socket: ServerConnection):
    await Signals.connected(socket)
    token = await socket.recv(decode=True)
    try:
        user_id = await check_token(token)
        await Signals.authenticated(socket)
    except SecurityServiceConnectionError:
        await Rejects.SecurityServiceConnectionError(socket)
        return
    except InvalidToken:
        await Rejects.InvalidToken(socket)
        return

    if user_id in online:
        online[user_id][1].cancel()
        await online[user_id][0].close()
    try:
        online[user_id] = (socket, asyncio.create_task(relay(socket, user_id)))
        await add_to_storage(user_id, str(socket.id))
        await socket.wait_closed()
        await Signals.disconnected(socket)
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"клиент {user_id}::{socket.id} отключился")
    finally:
        online[user_id][1].cancel()
        del online[user_id]
        async with online_user_storage as ous:
            await ous.delete(user_id)


#     error = None
#     await Signals.connected(socket)
#     token = await socket.recv(decode=True)
#
#     try:
#         user_id = await check_token(token)
#     except SecurityServiceConnectionError:
#         await Rejects.SecurityServiceConnectionError(socket)
#         return
#     except InvalidToken:
#         await Rejects.InvalidToken(socket)
#         return
#     try:
#         await add_to_storage(user_id, str(socket.id))
#         await Signals.authenticated(socket)
#         async with messages_transfer as connection:
#             p: PubSub = connection.pubsub()
#             if user_id in online:
#                 await start_crash_old_loop_process(connection, p, user_id)
#                 await Signals.restart(socket)
#             online[user_id] = socket.id
#             logger.debug(f"новый клиент {user_id}::{socket.id} сохранен")
#             await p.subscribe(f"message_to_{user_id}", "system")
#             while True:
#                 message = await p.get_message()
#                 logger.debug(f"получено сообщение {message}")
#                 if message and not isinstance(message["data"], int):
#                     if message["channel"].decode() == "system":
#                         if message["data"].decode() == "stop":
#                             # await kill_old_loop_procedure(socket, connection, p, user_id)
#                             break
#                     await socket.send(
#                         Event(type=EventTypes.MESSAGE, data=json.loads(message["data"].decode())).model_dump_json(),
#                         text=True)
#                 await socket.ping()
#                 await asyncio.sleep(1.5)
#                 logger.debug(online)
#                 logger.debug(socket.id)
#     except redis.exceptions.ConnectionError as e:
#         error = e
#         await Rejects.RedisConnectionError(socket)
#     except websockets.exceptions.ConnectionClosed:
#         print(f"{socket.id} disconnected")
#     finally:
#         logger.debug("начата процедура выхода из обрабоччика")
#         logger.debug("ищем сохраненный сокет в списке online клиентов")
#         # for uid, sid in online:
#         #     if socket.id == sid:
#         #         logger.debug("сокет найден")
#         #         del online[uid]
#         #         logger.debug(f"клиент {uid}::{sid} удален")
#         #         break
#
#         del online[user_id]
#         logger.debug("клиент удален из онлайн списка")
#         await kill_old_loop_procedure(socket, connection, p, user_id)
#
#         if not isinstance(error, redis.exceptions.ConnectionError):
#             async with online_user_storage as ous:
#                 await ous.delete(user_id)


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    if platform.system() != "Windows":
        loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    async with serve(handler, config.settings.SERVER_HOST, config.settings.SERVER_PORT):
        logger.info(f"server running ws://{config.settings.SERVER_HOST}:{config.settings.SERVER_PORT}")
        await stop


if __name__ == "__main__":
    config.is_dev(True if "dev" in sys.argv else False)
    asyncio.run(main())
