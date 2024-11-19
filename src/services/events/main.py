#!/usr/bin/env python

import asyncio

import redis
import websockets.exceptions
from pydantic import BaseModel
from redis.asyncio.client import PubSub
from websockets.asyncio.server import serve, ServerConnection

import config
from core.storage import RedisStorage

messages_transfer = RedisStorage(config.MESSAGES_STORAGE_DSN, config.MESSAGES_STORAGE_DB_NAME)


class TokenManager(BaseModel):
    pass


async def check_token(token) -> int:
    try:
        return TokenManager.decode(token)
    except websockets.exceptions.WebSocketException:
        raise websockets.exceptions.SecurityError()


online = {}


async def handler(socket: ServerConnection):
    # print(1)
    # token = await socket.recv(decode=True)
    # user_id = check_token(token)
    user_id = 1 + len(online)
    print("start")
    try:
        async with messages_transfer as connection:
            p: PubSub = connection.pubsub()
            if user_id in online:
                print(f'user {user_id} already exists')
                await p.subscribe("system")
                await connection.publish("system", "stop")
                while True:
                    message = await p.get_message()
                    if message:
                        print(f" pre loop {message}")
                        if not isinstance(message["data"], int):
                            print("data is exists")
                            if message["data"].decode() == "stopped":
                                print("stopped")
                                print("получили сигнал о завершении цикла")
                                await p.unsubscribe("system")
                                break

            online[user_id] = socket.id
            print(2)
            await p.subscribe("message", "system")
            while True:
                # message = await socket.recv(decode=True)
                message = await p.get_message()
                if message:
                    print(message)
                    if message["channel"].decode() == "system":
                        print(f"main loop {message}")
                        if not isinstance(message["data"], int):
                            if message["data"].decode() == "stop":
                                await socket.close()
                                await p.unsubscribe("message", "system")
                                del online[user_id]
                                await connection.publish("system", "stopped")
                                break
                    await socket.send(message["data"].decode(), text=True)
                # print(message)
                print(socket.id)
                print(f"online {online}")
                await socket.send("ping")

                await asyncio.sleep(2)
    except redis.exceptions.ConnectionError:
        await socket.send("redis отвалился", text=True)
    except websockets.exceptions.ConnectionClosed:
        print(f"{socket.id} отключился")
    finally:
        if user_id in online:
            del online[user_id]


async def main():
    async with serve(handler, config.SERVER_HOST, config.SERVER_PORT):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
