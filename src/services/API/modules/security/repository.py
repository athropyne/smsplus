from functools import wraps
from typing import Callable

import sqlalchemy
from fastapi import Depends, HTTPException
from sqlalchemy import CursorResult
from starlette import status

from core.utils import catch
from modules.security.stmts import Statement
from core.storages import Database


class Repository:

    def __init__(self,
                 stmt: Statement = Depends(Statement),
                 database: Database = Depends(Database)):
        self.stmt = stmt
        self.engine = database()

    @catch
    async def get_by_login(self, login: str):
        """Получает все поля пользователя по логину"""
        async with self.engine.connect() as c:
            cursor: CursorResult = await c.execute(self.stmt.get_by_login(login))
        return cursor.mappings().fetchone()
