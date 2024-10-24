from fastapi import Depends

from src.modules.messages.dto import CreateModel
from src.modules.messages.repository import Repository


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository)):
        self.repository = repository

    async def create(self, _from: int, model: CreateModel):
        data = model.model_dump()
        data["from"] = _from
        return await self.repository.create(data)

    async def get_history(self, self_id: int, interlocutor_id: int):
        return await self.repository.get_history(self_id, interlocutor_id)
