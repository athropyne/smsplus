import asyncio
import json

from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from starlette import status
from starlette.websockets import WebSocket

from src.core.security import TokenManager
from src.API.modules.messages.dto import CreateModel
from src.API.modules.messages.service import Service
from src.core.storages import message_transfer

router = APIRouter(prefix="/messages",
                   tags=["сообщения"])


@router.post("/{recipient_id}",
             status_code=status.HTTP_201_CREATED)
async def create(
        recipient_id: int,
        model: CreateModel,
        self_id: int = Depends(TokenManager.decode),
        service: Service = Depends(Service)):
    await service.create(self_id, recipient_id, model)


@router.get("/",
            description="получить историю сообщений")
async def get_history(
        self_id: int = Depends(TokenManager.decode),
        interlocutor_id: int = ...,
        service: Service = Depends(Service)
):
    return await service.get_history(self_id, interlocutor_id)


@router.websocket("/ws")
async def handler(websocket: WebSocket,
                  transfer: Redis = Depends(message_transfer)):
    await websocket.accept()
    p = transfer.pubsub()
    await p.subscribe("message")
    while True:
        msg = await p.get_message()
        print(msg)
        if msg is not None:
            if msg["data"] != 1:
                await websocket.send_text(msg["data"])
                # print(msg["data"])
        await asyncio.sleep(1)
