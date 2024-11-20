import aiohttp
import websockets
from redis.asyncio import Redis
from redis.asyncio.client import PubSub

import config


class Service:
    def __init__(self):
        ...

    async def check_token(self, token: str) -> int:
        # try:
            async with aiohttp.client.ClientSession() as session:
                async with session.post(f"{config.SECURITY_SERVER_DSN}/security/check",
                                        data=token) as response:
                    user_id = await response.text()
                    if response.status == 200:
                        return int(user_id)
                    raise websockets.exceptions.SecurityError()

        # except websockets.exceptions.WebSocketException as e:
        #     raise websockets.exceptions.SecurityError

    async def crash_old_loop(self, connection: Redis, p: PubSub):
        await p.subscribe("system")
        await connection.publish("system", "stop")
        while True:
            message = await p.get_message()
            if message:
                if not isinstance(message["data"], int):
                    if message["data"].decode() == "stopped":
                        await p.unsubscribe("system")
                        break
