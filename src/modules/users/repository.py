from sqlalchemy import CursorResult, select
from sqlalchemy.dialects.postgresql import insert

from src.core.interfaces import BaseRepository
from src.core.schemas import users


class Repository(BaseRepository):
    async def create(self, data: dict):
        cursor: CursorResult = await self.exec(
            insert(users)
            .values(data)
            .returning(users.c.id,
                       users.c.login)
        )
        return cursor.mappings().fetchone()

    async def list(self):
        cursor: CursorResult = await self.exec(
            select(
                users.c.id,
                users.c.login
            )
        )
        return cursor.mappings().fetchall()
