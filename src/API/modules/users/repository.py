import psycopg
from fastapi import HTTPException
from sqlalchemy import CursorResult, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.core.interfaces import BaseRepository
from src.core.schemas import users


class Repository(BaseRepository):
    async def create(self, data: dict):
        try:
            cursor: CursorResult = await self.exec(
                insert(users)
                .values(data)
                .returning(users.c.id,
                           users.c.login)
            )
            return cursor.mappings().fetchone()
        except IntegrityError as e:
            if isinstance(e.orig, psycopg.errors.UniqueViolation):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="пользователь уже существует")

    async def list(self):
        cursor: CursorResult = await self.exec(
            select(
                users.c.id,
                users.c.login
            )
        )
        return cursor.mappings().fetchall()
