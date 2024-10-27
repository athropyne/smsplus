from fastapi import APIRouter, Depends
from fastapi.params import Body
from fastapi.security import OAuth2PasswordRequestForm

from src.API.modules.security.service import Service
from src.core.security import TokenManager

router = APIRouter(prefix="/security")


@router.post("/sign_in", description="возвращает токен доступа")
async def sign_in(
        form: OAuth2PasswordRequestForm = Depends(),
        service: Service = Depends(Service)
):
    return await service.sign_in(form.username, form.password)

@router.post("/bind_tg", description="привязывает бот-уведомлятор к пользователю")
async def bind_tg(
        tg_id: int = Body(...),
        user_id: int = Depends(TokenManager.decode),
        service: Service = Depends(Service)
):
    return await service.bind_tg(user_id, tg_id)
