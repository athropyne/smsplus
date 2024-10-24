from sqlalchemy import CursorResult, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.operators import and_, or_

from src.core.interfaces import BaseRepository
from src.core.schemas import messages


class Repository(BaseRepository):
    async def create(self, data: dict):
        cursor: CursorResult = await self.exec(
            insert(messages)
            .values(data)
            .returning(messages)
        )
        return cursor.mappings().fetchone()

    async def get_history(self, self_id: int, interlocutor_id: int):
        cursor: CursorResult = await self.exec(
            select(messages)
            .where(
                or_(and_(messages.c["from"] == self_id,
                         messages.c.to == interlocutor_id),
                    and_(messages.c["from"] == interlocutor_id,
                         messages.c.to == self_id))
            )
            .order_by(messages.c.created_at)
        )
        return cursor.mappings().fetchall()
