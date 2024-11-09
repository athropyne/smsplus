from sqlalchemy import select, or_, and_
from sqlalchemy.dialects.postgresql import insert

from core.schemas import messages


class Statement:
    """Класс -- набор sql выражений"""

    def create(self, data: dict):
        return insert(messages).values(data).returning(messages)

    def get_history(self, self_id: int, interlocutor_id: int):
        return select(messages).where(
            or_(and_(messages.c.signal == self_id,
                     messages.c.receiver == interlocutor_id),
                and_(messages.c.signal == interlocutor_id,
                     messages.c.receiver == self_id))
        ).order_by(messages.c.created_at)
