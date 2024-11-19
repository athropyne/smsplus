from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm

from core.security import TokenManager
from modules.security.dto import TokenResponseModel
from modules.security.service import Service

router = APIRouter(prefix="/security")


@router.post("/sign_in",
             description="Аутентификация. Возвращает токен доступа",
             response_model=TokenResponseModel)
async def sign_in(
        form: OAuth2PasswordRequestForm = Depends(),
        service: Service = Depends(Service)
):
    return await service.sign_in(form.username, form.password)


@router.post("/refresh")
async def refresh(
        refresh_token: str = Body(...),
        service: Service = Depends(Service)
):
    return await service.refresh(refresh_token)


@router.post("/check")
async def check(
        token: str
) -> int:
    user_id = TokenManager.decode(token)
    return user_id
