from sqlalchemy import CursorResult, select, insert

from src.core.interfaces import BaseRepository
from src.core.schemas import users, tg


class Repository(BaseRepository):
    async def get_by_login(self, login: str):
        cursor: CursorResult = await self.exec(
            select(users)
            .where(users.c.login == login)
        )
        return cursor.mappings().fetchone()

    async def bind_tg(self, user_id: int, tg_id: int):
        cursor:CursorResult = await self.exec(
            insert(tg)
            .values(id=user_id, tg_id=tg_id)
            .returning(tg)
        )
        return cursor.mappings().fetchone()


