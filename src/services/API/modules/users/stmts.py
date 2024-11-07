from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from core.schemas import users, tg


class Statement:
    """Класс -- набор sql выражений"""

    def create(self, data: dict):
        return insert(users).values(data).returning(users.c.id, users.c.login)

    def list(self):
        return select(users.c.id, users.c.login)

    def get_login_by_id(self, user_id: int):
        return select(users.c.login).where(users.c.id == user_id)

    def bind_tg(self, user_id: int, tg_id: int):
        return insert(tg).values(id=user_id, tg_id=tg_id).returning(tg)

    def get_tg_ids_by_user_id(self, user_id: int):
        return select(tg.c.tg_id).where(tg.c.id == user_id)

