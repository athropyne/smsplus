from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.modules.security.service import Service

router = APIRouter(prefix="/security")


@router.post("/sign_in", description="возвращает токен доступа")
async def sign_in(
        form: OAuth2PasswordRequestForm = Depends(),
        service: Service = Depends(Service)
):
    return await service.sign_in(form.username, form.password)
