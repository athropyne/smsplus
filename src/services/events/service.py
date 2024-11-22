import aiohttp
from redis.asyncio import Redis
from redis.asyncio.client import PubSub
from websockets.asyncio.server import ServerConnection

from core import config
from core.storage import online_user_storage, online
from exc import SecurityServiceConnectionError, InvalidToken


class Service:

    @staticmethod
    async def check_token(token: str) -> int:
        try:
            async with aiohttp.client.ClientSession() as session:
                async with session.post(f"{config.settings.SECURITY_SERVER_DSN}/security/check",
                                        data=token) as response:
                    user_id = await response.text()
                    if response.status == 200:
                        return int(user_id)
                    raise InvalidToken

        except aiohttp.client_exceptions.ClientConnectorError as e:
            raise SecurityServiceConnectionError

    @staticmethod
    async def start_crash_old_loop_process(connection: Redis, p: PubSub):
        await p.subscribe("system")
        await connection.publish("system", "stop")
        while True:
            message = await p.get_message()
            if message:
                if not isinstance(message["data"], int):
                    if message["data"].decode() == "stopped":
                        await p.unsubscribe("system")
                        break

    @staticmethod
    async def kill_old_loop_procedure(socket: ServerConnection, redis: Redis, pubsub: PubSub, user_id: int):
        await socket.close()
        await pubsub.unsubscribe(f"message_to_{user_id}", "system")
        del online[user_id]
        await redis.publish("system", "stopped")

    @staticmethod
    async def add_to_storage(user_id: int, socket_id: str):
        async with online_user_storage as connection:
            await connection.set(user_id, socket_id)

