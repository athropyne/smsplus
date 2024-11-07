from datetime import timedelta

from core import config
from core.security import TokenManager
from modules.security.dto import TokenResponseModel


class Helper:
    def get_token_model(self, user_id: int) -> TokenResponseModel:
        """Возвращает токен доступа и токен обновления в виде модели"""
        access_token = TokenManager.create({"sub": user_id}, timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES()))
        refresh_token = TokenManager.create({"sub": user_id}, timedelta(hours=config.REFRESH_TOKEN_EXPIRE_HOURS()))
        return TokenResponseModel(
            **{"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token})
