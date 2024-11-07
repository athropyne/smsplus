from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from core.storages import Database


# class BaseRepository:
#     def __init__(self,
#                  database: Database = Depends(Database)):
#         self.engine: AsyncEngine = database()




