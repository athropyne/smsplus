import logging
from typing import Dict

import redis
from redis.asyncio import Redis
from websockets.asyncio.server import ServerConnection

from core import config


class RedisStorage:

    def __init__(self,
                 dsn: str):
        self._pool: redis.asyncio.ConnectionPool = redis.asyncio.ConnectionPool.from_url(dsn)
        self.connection: Redis = Redis(connection_pool=self._pool, decode_responses=True)

    async def __aenter__(self):
        self.connection = Redis(connection_pool=self._pool)
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()

    async def __call__(self):
        return self


messages_transfer = RedisStorage(config.settings.MESSAGE_TRANSFER_DSN)
online_user_storage = RedisStorage(config.settings.ONLINE_USER_STORAGE_DSN)
token_storage = RedisStorage(config.settings.TOKEN_STORAGE_DSN)

online = {}
