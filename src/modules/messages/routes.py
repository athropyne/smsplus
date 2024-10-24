from fastapi import APIRouter, Depends
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.core.security import TokenManager
from src.core.storages import WSStorage
from src.modules.messages.dto import CreateModel
from src.modules.messages.service import Service

router = APIRouter(prefix="/messages",
                   tags=["сообщения"])


@router.post("/",
             status_code=status.HTTP_201_CREATED)
async def create(model: CreateModel,
                 self_id: int = Depends(TokenManager.decode),
                 service: Service = Depends(Service)):
    await service.create(self_id, model)


@router.get("/",
            description="получить историю сообщений")
async def get_history(
        self_id: int = Depends(TokenManager.decode),
        interlocutor_id: int = ...,
        service: Service = Depends(Service)
):
    return await service.get_history(self_id, interlocutor_id)
