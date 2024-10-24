from fastapi import Depends

from src.core.security import PasswordManager
from src.modules.users.dto import CreateModel
from src.modules.users.repository import Repository


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository)):
        self.repository = repository

    async def create(self, model: CreateModel):
        model.password = PasswordManager.hash(model.password)
        return await self.repository.create(model.model_dump())

    async def list(self):
        return await self.repository.list()
