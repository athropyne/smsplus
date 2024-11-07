import logging
from typing import Sequence

from fastapi import Depends
from sqlalchemy import RowMapping

from modules.users.cache import Cache
from modules.users.dto import CreateModel
from modules.users.helper import Helper
from modules.users.repository import Repository
from core.security import PasswordManager


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository),
                 cache: Cache = Depends(Cache),
                 helper: Helper = Depends(Helper)):
        self.repository = repository
        self.cache = cache
        self.helper = helper

    async def create(self, model: CreateModel):
        model.password = PasswordManager.hash(model.password)
        result = await self.repository.create(model.model_dump())
        try:
            await self.cache.add(list(result.values()))
        except:
            logging.warning("ошибка сохранения в кэш")
        return result

    async def list(self):
        try:
            users: dict = await self.cache.list()
            if len(users):
                return await self.helper.decode_user_list_for_response(users)
        except:
            logging.warning("ошибка извлечения из кэша")
        users: Sequence[RowMapping] = await self.repository.list()
        try:
            await self.cache.fill(await self.helper.convert_users_list_for_redis(users))
        except:
            logging.warning("ошибка заполнения кэша")
        return users

    async def bind_tg(self, user_id: int, tg_id: int):
        await self.repository.bind_tg(user_id, tg_id)
