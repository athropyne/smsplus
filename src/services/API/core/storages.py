from typing import Dict

import redis.asyncio
from redis.asyncio import Redis
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from starlette.websockets import WebSocket

from core import config


class Database:
    def __init__(self):
        self.engine = create_async_engine(config.PG_DSN(), echo=True)

    async def init(self, metadata: MetaData):
        async with self.engine.connect() as connection:
            # await connection.run_sync(metadata.drop_all)
            await connection.run_sync(metadata.create_all)
            await connection.commit()
        await self.engine.dispose()

    async def dispose(self):
        await self.engine.dispose()

    def __call__(self) -> AsyncEngine:
        return self.engine


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
    users: Dict[int, WebSocket] = {}

    @classmethod
    def add(cls, user_id: int, socket: WebSocket):
        cls.users[user_id] = socket

    @classmethod
    def remove(cls, user_id: int):
        if user_id in cls.users:
            del cls.users[user_id]

    @classmethod
    def get(cls, recipient_id: int) -> WebSocket:
        if recipient_id in cls.users:
            return cls.users[recipient_id]


users_cache = RedisStorage(config.REDIS_DSN(), config.USERS_CACHE_REDIS_DBNAME())
message_transfer = RedisStorage(config.REDIS_DSN(), config.MESSAGE_TRANSFER_REDIS_DBNAME())
