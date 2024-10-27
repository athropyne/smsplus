import asyncio
import json

import redis
from fastapi import Depends, HTTPException, WebSocketException
from redis.asyncio import Redis
from starlette import status
from starlette.websockets import WebSocket

from src.API.modules.messages.dto import CreateModel
from src.API.modules.messages.helpers import Helper
from src.API.modules.messages.repository import Repository
from src.core.storages import message_transfer, Online


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository),
                 transfer: Redis = Depends(message_transfer),
                 helper: Helper = Depends(Helper)):
        self.repository = repository
        self.transfer = transfer
        self.helper = helper

    async def create(self, _from: int, _to: int, model: CreateModel):
        data = model.model_dump()
        data["from"] = _from
        data["to"] = _to
        try:
            if Online.get(_to):
                ...  # create celery task for send message to tg bot
            await self.transfer.publish("message", json.dumps(data))
        except redis.exceptions.ConnectionError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="косячок на сервере. исправляем")
        return await self.repository.create(data)

    async def get_history(self, self_id: int, interlocutor_id: int):
        return await self.repository.get_history(self_id, interlocutor_id)

    async def exchange(self,
                       recipient_id: int,
                       recipient_socket: WebSocket):
        await recipient_socket.accept()
        Online.add(recipient_id, recipient_socket)
        p = self.transfer.pubsub()
        await p.subscribe("message")
        try:
            while True:
                msg = await p.get_message()
                if msg is not None:
                    print(msg)
                    if msg["data"] != 1:
                        data = json.loads(msg["data"])
                        sender_id = data["from"]
                        sender_login = await self.helper.convert_to_login(sender_id)
                        output = {
                            "from": sender_login,
                            "text": data["text"]
                        }
                        await recipient_socket.send_json(output)
                await asyncio.sleep(1)
        except WebSocketException:
            Online.remove(recipient_id)
