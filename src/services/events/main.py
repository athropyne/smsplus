#!/usr/bin/env python

import asyncio

import redis
import websockets.exceptions
from redis.asyncio.client import PubSub
from websockets.asyncio.server import serve, ServerConnection

import config
from core.storage import online, messages_transfer, online_user_storage
from dto import SystemMessage
from service import Service

service = Service()


async def handler(socket: ServerConnection):
    await socket.send(SystemMessage(signal="Подключено").model_dump_json())
    token = await socket.recv(decode=True)
    print(token)
    try:
        user_id = await service.check_token(token)
        async with online_user_storage as connection:
            await connection.set(user_id, str(socket.id))
        await socket.send(SystemMessage(signal="распозан").model_dump_json())

    except websockets.exceptions.SecurityError:
        await socket.send(SystemMessage(signal="неизвестный пользователь").model_dump_json())
        await socket.close(code=1011, reason="NOT AUTHORIZED")
        return
    print(user_id)
    try:
        async with messages_transfer as connection:
            p: PubSub = connection.pubsub()
            if user_id in online:
                await service.crash_old_loop(connection, p)

            online[user_id] = socket.id
            await p.subscribe(f"message_to_{user_id}", "system")
            while True:
                message = await p.get_message()
                if message:
                    if not isinstance(message["data"], int):
                        if message["channel"].decode() == "system":
                            if message["data"].decode() == "stop":
                                await socket.close()
                                async with online_user_storage as ous:
                                    await ous.delete(user_id)
                                await p.unsubscribe(f"message_to_{user_id}", "system")
                                del online[user_id]
                                await connection.publish("system", "stopped")
                                break
                        await socket.send(message["data"].decode(), text=True)
                await socket.ping()
                await asyncio.sleep(0.5)
    except redis.exceptions.ConnectionError:
        await socket.send("redis отвалился", text=True)
    except websockets.exceptions.ConnectionClosed:
        print(f"{socket.id} отключился")
    finally:
        async with online_user_storage as ous:
            await ous.delete(user_id)
        if user_id in online:
            del online[user_id]


async def main():
    async with serve(handler, config.SERVER_HOST, config.SERVER_PORT):
        print(f"server running ws://{config.SERVER_HOST}:{config.SERVER_PORT}")
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
