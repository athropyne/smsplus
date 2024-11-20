from typing import Dict

import redis
from redis.asyncio import Redis
from websockets.asyncio.server import ServerConnection

import config


class __RedisStorage:

    def __init__(self,
                 dsn: str,
                 db_name: int):
        self._pool: redis.asyncio.ConnectionPool = redis.asyncio.ConnectionPool.from_url(
            f"{dsn}/{db_name}"
        )
        self.connection: Redis = Redis(connection_pool=self._pool, decode_responses=True)

    async def __aenter__(self):
        self.connection = Redis(connection_pool=self._pool)
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()

    async def __call__(self):
        return self


messages_transfer = __RedisStorage(config.MESSAGES_TRANSFER_DSN, config.MESSAGES_TRANSFER_DB_NAME)
online_user_storage = __RedisStorage(config.ONLINE_USERS_STORAGE_DSN, config.ONLINE_USERS_STORAGE_DB_NAME)


class Online:
    def __init__(self):
        self._connections: Dict[int, ServerConnection] = {}

    def __setitem__(self, key, value):
        self._connections[key] = value

    def __getitem__(self, item):
        self._connections.get(item)

    def __delitem__(self, key):
        if key in self._connections:
            del self._connections

    def __contains__(self, item):
        return item in self._connections

    def __len__(self):
        return len(self._connections)


online = {}
