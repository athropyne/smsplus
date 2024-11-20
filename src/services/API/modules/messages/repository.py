from fastapi import Depends
from sqlalchemy import CursorResult

from core.utils import catch
from modules.messages.stmts import Statement
from core.storages import Database


# from core.interfaces import BaseRepository


class Repository:

    def __init__(self,
                 stmt: Statement = Depends(Statement),
                 database: Database = Depends(Database)):
        self.engine = database()
        self.stmt = stmt

    @catch
    async def create(self, data: dict):
        """Сохраняет в базе новое сообщение и возвращает всю инфу о нем"""
        async with self.engine.connect() as c:
            cursor: CursorResult = await c.execute(self.stmt.create(data))
            await c.commit()
        return cursor.mappings().fetchone()

    @catch
    async def get_history(self, self_id: int, interlocutor_id: int):
        """Получает всю историю сообщений между двумя пользователями, отсортированную по дате"""
        async with self.engine.connect() as c:
            cursor: CursorResult = await c.execute(self.stmt.get_history(self_id, interlocutor_id))
        return cursor.mappings().fetchall()
