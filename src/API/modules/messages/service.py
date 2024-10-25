import json

import redis
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis
from starlette import status

from src.API.modules.messages.dto import CreateModel
from src.API.modules.messages.repository import Repository
from src.core.storages import message_transfer


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository),
                 transfer: Redis = Depends(message_transfer)):
        self.repository = repository
        self.transfer = transfer

    async def create(self, _from: int,_to: int, model: CreateModel):
        data = model.model_dump()
        data["from"] = _from
        data["to"] = _to
        try:
            await self.transfer.publish("message",json.dumps(data))
        except redis.exceptions.ConnectionError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="косячок на сервере. исправляем") # на самом деле нихрена мы не испраляем
            # тут по хорошему нужно косячок записать в лог и отправить уведомление себе куда нибудь, в тг бот, например
            # это тестовое так что делать я этого не стану ;)
        return await self.repository.create(data)

    async def get_history(self, self_id: int, interlocutor_id: int):
        return await self.repository.get_history(self_id, interlocutor_id)
