#!/usr/bin/env python

import asyncio

import websockets.exceptions
from pydantic import BaseModel
from websockets import WebSocketException
from websockets.asyncio.server import serve, ServerConnection

import config


class TokenManager(BaseModel):
    pass


async def check_token(token) -> int:
    try:
        return TokenManager.decode(token)
    except websockets.exceptions.WebSocketException:
        raise websockets.exceptions.SecurityError()


async def handler(socket: ServerConnection):
    token = await socket.recv(decode=True)
    user_id = check_token(token)
    while True:
        message = await socket.recv()
        print(message)


async def main():
    async with serve(handler, config.SERVER_HOST, config.SERVER_PORT):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
