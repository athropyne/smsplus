from typing import List

from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket

from modules.messages.dto import MessageModel
from modules.messages.service import Service
# from modules.messages.service import Service, EventService
from core.security import TokenManager

router = APIRouter(prefix="/messages",
                   tags=["сообщения"])


@router.get("/",
            description="Получить историю сообщений",
            response_model=List[MessageModel])
async def get_history(
        self_id: int = Depends(TokenManager.decode),
        interlocutor_id: int = ...,
        service: Service = Depends(Service)
):
    return await service.get_history(self_id, interlocutor_id)


@router.websocket("/ws/{token}")
async def exchange(
        token: str,
        recipient_socket: WebSocket,
        service: Service = Depends(Service)):
    recipient_id: int = TokenManager.decode(token)
    await service.exchange(recipient_id, recipient_socket)
