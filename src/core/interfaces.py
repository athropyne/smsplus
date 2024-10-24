from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection

from src.core.storages import Database


class BaseRepository:
    def __init__(self,
                 connection: AsyncConnection = Depends(Database.connect)):
        self.connection = connection
        self.exec: Callable = connection.execute

    async def commit(self):
        await self.connection.commit()

    async def close(self):
        await self.connection.close()

    async def finish(self):
        await self.commit()
        await self.close()



