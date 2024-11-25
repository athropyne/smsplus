from typing import List

from fastapi import APIRouter, Depends
from fastapi.params import Body
from starlette.websockets import WebSocket

from modules.messages.dto import MessageModel
from modules.messages.service import Service
# from modules.messages.service import Service, EventService
from core.security import TokenManager

router = APIRouter(prefix="/messages",
                   tags=["сообщения"])


@router.post("/{receiver_id}",
             description="отправляет сообщение")
async def send(
        receiver_id: int,
        text: str = Body(..., max_length=300),
        sender_id: int = Depends(TokenManager.decode),
        service: Service = Depends(Service)):
    print(sender_id)
    return await service.send(sender_id, receiver_id, text)



@router.get("/",
            description="Получить историю сообщений",
            response_model=List[MessageModel])
async def get_history(
        self_id: int = Depends(TokenManager.decode),
        interlocutor_id: int = ...,
        service: Service = Depends(Service)
):
    return await service.get_history(self_id, interlocutor_id)


# @router.websocket("/ws")
# async def exchange(
#         recipient_socket: WebSocket,
#         service: Service = Depends(Service)):
#     await service.exchange(recipient_socket)
