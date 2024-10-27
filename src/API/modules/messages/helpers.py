from fastapi import Depends, HTTPException
from redis.asyncio import Redis
from starlette import status

from src.API.modules.users.repository import Repository
from src.core.storages import users_cache


class Helper:
    def __init__(self,
                 user_repository: Repository = Depends(Repository),
                 cache: Redis = Depends(users_cache)):
        self.user_repository = user_repository
        self.user_cache = cache

    async def convert_to_login(self, user_id: int) -> str:
        user_login = await self.user_cache.get(str(user_id))
        if user_login is None:
            user_login = await self.user_repository.get_login_by_id(user_id)
            await self.user_cache.set(str(user_id), user_login, ex=30*60) # 30 минут в кэше
            if user_login is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"пользователя с ID {user_id} не существует")
        return user_login
