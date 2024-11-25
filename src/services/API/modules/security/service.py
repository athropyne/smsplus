from fastapi import Depends
from sqlalchemy import RowMapping

from core.security import TokenManager
from modules.security.dto import TokenResponseModel
from modules.security.helpers import Helper
from modules.security.repository import Repository
from modules.security.utils import check_user, compare_passwords, add_access_token_to_storage


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository),
                 helper: Helper = Depends(Helper)):
        self.repository = repository
        self.helper = helper

    async def sign_in(self, login: str, password: str) -> TokenResponseModel:
        """Достает из базы данные пользователя сверяет приходящий пароль с сохраненным.
        Возвращает 400 если пароли не совпадают или пользователя не существует.
        Возвращает токен доступа если все круто классно.
        """
        user: RowMapping = await self.repository.get_by_login(login)
        check_user(user)
        compare_passwords(password, user["password"])
        token_response_model: TokenResponseModel = self.helper.get_token_model(user["id"])
        await add_access_token_to_storage(token_response_model.access_token, user["id"])
        return token_response_model

    async def refresh(self, refresh_token: str) -> TokenResponseModel:
        """ Обновляет access и refresh токены, добавляет новый access в кэш и возвращает оба токена в виде
        TokenResponseModel"""
        user_id: int = TokenManager.decode(refresh_token)
        token_response_model = self.helper.get_token_model(user_id)
        await add_access_token_to_storage(token_response_model.access_token, user_id)
        return token_response_model
