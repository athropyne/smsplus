from typing import Dict

import redis
from redis.asyncio import Redis
from websockets.asyncio.server import ServerConnection


class RedisStorage:

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


class Online:
    _connections: Dict[int, ServerConnection] = {}

    @classmethod
    def __setitem__(cls, key, value):
        cls._connections[key] = value

    @classmethod
    def __getitem__(cls, item):
        cls._connections.get(item)

    @classmethod
    def __delitem__(cls, key):
        if key in cls._connections:
            del cls._connections

    @classmethod
    def __contains__(cls, item):
        return item in cls._connections

