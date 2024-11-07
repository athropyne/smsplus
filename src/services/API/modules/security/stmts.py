from sqlalchemy import select

from core.schemas import users


class Statement:
    """Класс -- набор sql выражений"""

    def get_by_login(self, login: str):
        return select(users).where(users.c.login == login)
