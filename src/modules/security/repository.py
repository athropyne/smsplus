from sqlalchemy import CursorResult, select

from src.core.interfaces import BaseRepository
from src.core.schemas import users


class Repository(BaseRepository):
    async def get_by_login(self, login: str):
        cursor: CursorResult = await self.exec(
            select(users)
            .where(users.c.login == login)
        )
        return cursor.mappings().fetchone()
