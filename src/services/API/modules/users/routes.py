from typing import List

from fastapi import APIRouter, Depends, Body
from starlette import status

from core import security
from modules.users.dto import UserInfoModel, CreateModel
from modules.users.service import Service
from core.security import TokenManager

router = APIRouter(prefix="/users",
                   tags=["пользователи"])


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=UserInfoModel,
             description="Регистрация нового пользователя")
async def create(
        model: CreateModel,
        service: Service = Depends(Service)
):
    return await service.create(model)


@router.get("/",
            response_model=List[UserInfoModel],
            dependencies=[Depends(security.auth_scheme)],
            description="получает список пользователей с логинами и айдишниками")
async def get_list(service: Service = Depends(Service)):
    return await service.list()


@router.post("/bind_tg",
             status_code=status.HTTP_201_CREATED,
             description="привязывает бот-уведомлятор к пользователю."
                         "НЕБЕЗОПАСНАЯ ФУНКЦИЯ!  По факту можно привязать любой telegramID к любому пользователю."
                         "Чинится сия дыра множеством способов: двойным рукопожатием между сервером и ботом,"
                         "проверкой заголовков запроса,"
                         "отправкой проверочного кода на сторойнний сервис (почта например)."
                         "Но я не буду на это тратить время :) . . . "
                         "Возвращает 201 в случае успеха")
async def bind_tg(
        tg_id: int = Body(..., description="ID телеги"),
        user_id: int = Depends(TokenManager.decode),
        service: Service = Depends(Service)
):
    return await service.bind_tg(user_id, tg_id)
