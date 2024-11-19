#!/usr/bin/env python

import asyncio

import aiohttp
import redis
import websockets.exceptions
from pydantic import BaseModel
from redis.asyncio.client import PubSub
from websockets.asyncio.server import serve, ServerConnection

import config
from core.storage import RedisStorage, Online

messages_transfer = RedisStorage(config.MESSAGES_STORAGE_DSN, config.MESSAGES_STORAGE_DB_NAME)


class TokenManager(BaseModel):
    pass


async def check_token(token) -> int:
    try:
        async with aiohttp.client.ClientSession as session:
            async with session.post(f"{config.SECURITY_SERVER_DSN}/security/check_token",
                                    data=token) as response:
                user_id = await response.text()
        return int(user_id)

    except websockets.exceptions.WebSocketException:
        raise websockets.exceptions.SecurityError()


# online = {}


async def handler(socket: ServerConnection):
    token = await socket.recv(decode=True)
    user_id = check_token(token)

    try:
        async with messages_transfer as connection:
            p: PubSub = connection.pubsub()
            if user_id in Online:
                await p.subscribe("system")
                await connection.publish("system", "stop")
                while True:
                    message = await p.get_message()
                    if message:
                        if not isinstance(message["data"], int):
                            if message["data"].decode() == "stopped":
                                await p.unsubscribe("system")
                                break

            Online[user_id] = socket.id
            await p.subscribe("message", "system")
            socket_id = socket.id
            while True:
                message = await p.get_message()
                if message:
                    if not isinstance(message["data"], int):
                        print(f"main loop {message}")

                        if message["channel"].decode() == "system":
                            if message["data"].decode() == "stop":
                                await socket.close()
                                await p.unsubscribe("message", "system")
                                del Online[user_id]
                                await connection.publish("system", "stopped")
                                break
                        await socket.send(message["data"].decode(), text=True)
                await socket.ping()
                print(socket_id)
                await asyncio.sleep(2)
    except redis.exceptions.ConnectionError:
        await socket.send("redis отвалился", text=True)
    except websockets.exceptions.ConnectionClosed:
        print(f"{socket.id} отключился")
    finally:
        if user_id in Online:
            del Online[user_id]


async def main():
    async with serve(handler, config.SERVER_HOST, config.SERVER_PORT):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
