import psycopg
from fastapi import HTTPException, Depends
from sqlalchemy import CursorResult
from sqlalchemy.exc import IntegrityError
from starlette import status

from modules.users.stmts import Statement
from core.storages import Database


class Repository:

    def __init__(self, stmt: Statement = Depends(Statement),
                 database: Database = Depends(Database)):
        super().__init__()
        self.stmt = stmt
        self.engine = database()

    async def create(self, data: dict):
        """Сохраняет пользователя в базу. Возвращает 400 если логин уже существует"""
        try:
            async with self.engine.connect() as c:
                cursor: CursorResult = await c.execute(self.stmt.create(data))
                await c.commit()
            return cursor.mappings().fetchone()
        except IntegrityError as e:
            if isinstance(e.orig, psycopg.errors.UniqueViolation):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="пользователь уже существует")

    async def list(self):
        """Возвращает список пользователей - логины и ID"""
        async with self.engine.connect() as c:
            cursor: CursorResult = await c.execute(self.stmt.list())
        return cursor.mappings().fetchall()

    async def get_login_by_id(self, user_id: int) -> str:
        """Получает логин пользователя по ид"""
        async with self.engine.connect() as c:
            cursor: CursorResult = await c.execute(self.stmt.get_login_by_id(user_id))
        return cursor.scalar()

    async def bind_tg(self, user_id: int, tg_id: int):
        """Привязывает пользоваеля к телеграм для отправки уведомлений"""
        try:
            async with self.engine.connect() as c:
                cursor: CursorResult = await c.execute(self.stmt.bind_tg(user_id, tg_id))
                await c.commit()
            return cursor.mappings().fetchone()
        except IntegrityError as e:
            if isinstance(e.orig, psycopg.errors.UniqueViolation):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="вы уже привязаны"
                )

    async def get_tg_ids_by_user_id(self, user_id: int):
        """Получает все привязанные TelegramID к ID пользователя"""
        async with self.engine.connect() as c:
            cursor: CursorResult = await c.execute(self.stmt.get_tg_ids_by_user_id(user_id))
            return cursor.scalars()
