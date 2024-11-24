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
                 helper: Helper = Depends(Helper)):
        self.repository = repository
        self.helper = helper

    async def create(self, model: CreateModel) -> RowMapping:
        model.password = PasswordManager.hash(model.password)
        return await self.repository.create(model.model_dump())

    async def list(self) -> Sequence[RowMapping]:
        return await self.repository.list()

    async def bind_tg(self, user_id: int, tg_id: int):
        await self.repository.bind_tg(user_id, tg_id)
