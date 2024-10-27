from fastapi import APIRouter, Depends
from starlette import status
from starlette.websockets import WebSocket

from src.API.modules.messages.dto import CreateModel
from src.API.modules.messages.service import Service
from src.core.security import TokenManager

router = APIRouter(prefix="/messages",
                   tags=["сообщения"])


@router.post("/{recipient_id}",
             status_code=status.HTTP_201_CREATED)
async def create(
        recipient_id: int,
        model: CreateModel,
        self_id: int = Depends(TokenManager.decode),
        service: Service = Depends(Service)):
    print(recipient_id)
    print(self_id)
    await service.create(self_id, recipient_id, model)


@router.get("/",
            description="получить историю сообщений")
async def get_history(
        self_id: int = Depends(TokenManager.decode),
        interlocutor_id: int = ...,
        service: Service = Depends(Service)
):
    print(" from ws route " + str(self_id))
    return await service.get_history(self_id, interlocutor_id)


@router.websocket("/ws")
async def exchange(recipient_socket: WebSocket,
                   recipient_id: int = Depends(TokenManager.decode),
                   service: Service = Depends(Service)):
    print(str(recipient_id) + " from route")
    await service.exchange(recipient_id, recipient_socket)
