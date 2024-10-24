from typing import Dict

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


class WSStorage:
    _online: Dict[int, WebSocket] = {}

    @classmethod
    def add(cls, user_id: int, socket: WebSocket):
        cls._online[user_id] = socket

    @classmethod
    def delete(cls, user_id: int):
        del cls._online[user_id]
