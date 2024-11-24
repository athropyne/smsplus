from datetime import timedelta

from core import config
from core.security import TokenManager, TokenTypes
from modules.security.dto import TokenResponseModel


class Helper:
    def get_token_model(self, user_id: int) -> TokenResponseModel:
        """Возвращает токен доступа и токен обновления в виде модели"""
        access_token = TokenManager.create({"sub": user_id}, TokenTypes.ACCESS)
        refresh_token = TokenManager.create({"sub": user_id}, TokenTypes.REFRESH)
        return TokenResponseModel(**{"access_token": access_token,
                                     "token_type": "bearer",
                                     "refresh_token": refresh_token})
