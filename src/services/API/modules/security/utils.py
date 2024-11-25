from sqlalchemy import RowMapping

from core.security import PasswordManager, TokenManager
from core.storages import token_storage
from modules.security.exc import UserNotFound, InvalidPassword


def check_user(user: RowMapping):
    if user is None:
        raise UserNotFound


def compare_passwords(plain: str, hashed: str):
    if not PasswordManager.verify(plain, hashed):
        raise InvalidPassword


async def add_access_token_to_storage(access_token: str, user_id: int):
    async with token_storage as connection:
        await connection.set(access_token,
                             user_id,
                             ex=TokenManager.ACCESS_TOKEN_EXPIRE_SECOND)
