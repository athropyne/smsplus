import redis.exceptions
import websockets.exceptions
from redis.asyncio import Redis
from redis.asyncio.client import PubSub
from websockets.asyncio.server import ServerConnection

from core.config import logger
from core.storage import online_user_storage, online, token_storage
from exc import SecurityServiceConnectionError, InvalidToken


async def check_token(token: str) -> int:
    try:
        logger.debug("попытка связаться с сервисом аутентификации")
        async with token_storage as connection:
            user_id = await connection.get(token)
            logger.debug(f"получен user id {user_id}")
        if user_id is None:
            raise InvalidToken
        return int(user_id.decode())
    except redis.exceptions.ConnectionError:
        raise SecurityServiceConnectionError


async def start_crash_old_loop_process(connection: Redis, p: PubSub, user_id: int):
    logger.debug("начало процесса уничтожения старого цикла")
    await p.subscribe(f"system_to_{user_id}")
    logger.debug("подписались на системный канал")
    await connection.publish(f"system_to_{user_id}", "stop")
    logger.debug("отправили сигнал stop в старый цикл")
    logger.debug("начинаем ждать ответный сигнал")
    while True:
        logger.debug("ждем сигнал stopped")
        message = await p.get_message(ignore_subscribe_messages=True)
        if message:
            logger.debug(f"получено сообщение {message}")
            if not isinstance(message["data"], int):
                if message["data"].decode() == "stopped":
                    logger.debug("получили подтверждение закрытия старого цикла")
                    await p.unsubscribe(f"system_to_{user_id}")
                    break


async def kill_old_loop_procedure(socket: ServerConnection, storage: Redis, pubsub: PubSub, user_id: int):
    logger.debug("старт процедуры уничтожения цикла")
    await socket.close()
    await socket.wait_closed()
    logger.debug("старый сокет закрыт")
    try:
        await pubsub.unsubscribe(f"message_to_{user_id}", f"system_to_{user_id}")
        await storage.publish(f"system_to_{user_id}", "stopped")
        logger.debug("сигнал stopped отправлен в новое подключение")
    except redis.exceptions.ConnectionError:
        logger.error("redis не доступен, сигнал в новое подключение не отправлен",
                     stack_info=True)


async def add_to_storage(user_id: int, socket_id: str):
    try:
        async with online_user_storage as connection:
            await connection.set(user_id, socket_id)
        logger.info(f"подключение {user_id}::{socket_id} сохранено в хранилище")
    except redis.exceptions.ConnectionError as e:
        logger.critical(
            f"подключение {user_id}::{socket_id} НЕ сохранено в хранилище из за недоступности сервиса online_user_storage")
        raise websockets.exceptions.WebSocketException
