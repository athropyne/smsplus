from typing import Dict

import redis.asyncio
from redis.asyncio import Redis
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from starlette.websockets import WebSocket

from src.core import config


class Database:
    engine = create_async_engine(config.PG_DSN, echo=True)
    _autocommit = config.PG_TRANSACTIONS_AUTOCOMMIT()

    @classmethod
    async def init(cls, metadata: MetaData):
        async with cls.engine.connect() as connection:
            # await connection.run_sync(metadata.drop_all)
            await connection.run_sync(metadata.create_all)
            await connection.commit()
        await cls.engine.dispose()

    @classmethod
    async def connect(cls):
        async with cls.engine.connect() as connection:
            yield connection
            if cls._autocommit:
                await connection.commit()

    @classmethod
    async def dispose(cls):
        await cls.engine.dispose()


class RedisStorage:

    def __init__(self,
                 host: str,
                 port: int,
                 db):
        self.connection: Redis = redis.asyncio.Redis(host=host,
                                                     port=port,
                                                     db=db,
                                                     decode_responses=True)

    async def __call__(self):
        return self.connection


message_transfer = RedisStorage(config.REDIS_HOST(),
                                config.REDIS_PORT(),
                                config.REDIS_DBNAME())
