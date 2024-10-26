from typing import Dict

import redis.asyncio
from fastapi import WebSocketException
from redis.asyncio import Redis
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from starlette import status
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


users_cache = RedisStorage(config.USERS_CACHE_REDIS_HOST(),
                           config.USERS_CACHE_REDIS_PORT(),
                           config.USERS_CACHE_REDIS_DBNAME())

message_transfer = RedisStorage(config.MESSAGE_TRANSFER_REDIS_HOST(),
                                config.MESSAGE_TRANSFER_REDIS_PORT(),
                                config.MESSAGE_TRANSFER_REDIS_DBNAME())


class Online:
    _users: Dict[int, WebSocket] = {}

    @classmethod
    def add(cls, user_id: int, socket: WebSocket):
        cls._users[user_id] = socket

    @classmethod
    def remove(cls, user_id: int):
        if user_id in cls._users:
            del cls._users[user_id]

    @classmethod
    def get(cls, recipient_id: int) -> WebSocket:
        if recipient_id in cls._users:
            return cls._users[recipient_id]
        raise WebSocketException(
            code=status.WS_1003_UNSUPPORTED_DATA,
            reason="пользователь оффлайн или не существует"
        )
