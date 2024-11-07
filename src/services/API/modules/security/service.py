from datetime import timedelta

from fastapi import Depends, HTTPException
from starlette import status

from modules.security.dto import TokenResponseModel
from core import config
from core.security import PasswordManager, TokenManager
from modules.security.helpers import Helper
from modules.security.repository import Repository


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository),
                 helper: Helper = Depends(Helper)):
        self.repository = repository
        self.helper = helper

    async def sign_in(self, login: str, password: str):
        """Достает из базы данные пользователя сверяет приходящий пароль с сохраненным.
        Возвращает 404 если пользователя с указанным логином нет.
        Возвращает 400 если пароли не совпадают.
        Возвращает токен доступа если все круто классно.
        """
        user = await self.repository.get_by_login(login)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="user not found")

        if not PasswordManager.verify(password, user["password"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="invalid login or password")
        return self.helper.get_token_model(user["id"])

    async def refresh(self, refresh_token: str):
        user_id = TokenManager.decode(refresh_token)
        return self.helper.get_token_model(user_id)
