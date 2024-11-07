from fastapi import Depends, HTTPException
from starlette import status

from core.storages import users_cache, RedisStorage
from modules.messages.dto import MessageModel
from modules.users.repository import Repository


class Helper:
    def __init__(self,
                 user_repository: Repository = Depends(Repository),
                 storage: RedisStorage = Depends(users_cache)):
        self.user_repository = user_repository
        self.storage = storage

    async def get_message_model(self, sender_id: int, receiver_id: int, text: str):
        return MessageModel(text=text, sender=sender_id, receiver=receiver_id)

    async def convert_to_login(self, user_id: int) -> str:
        async with self.storage as c:
            user_login = await c.get(str(user_id))
        if user_login is None:
            user_login = await self.user_repository.get_login_by_id(user_id)
            await c.set(str(user_id), user_login, ex=30 * 60)  # 30 минут в кэше
            if user_login is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"пользователя с ID {user_id} не существует")
        return user_login

    async def get_tg_id(self, user_id: int):
        return await self.user_repository.get_tg_ids_by_user_id(user_id)
