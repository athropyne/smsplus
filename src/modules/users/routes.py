from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.core import security
from src.core.security import TokenManager
from src.modules.users.dto import UserInfoModel, CreateModel
from src.modules.users.service import Service

router = APIRouter(prefix="/users",
                   tags=["пользователи"])


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=UserInfoModel)
async def create(
        model: CreateModel,
        service: Service = Depends(Service)
):
    return await service.create(model)


@router.get("/",
            response_model=List[UserInfoModel],
            dependencies=[Depends(security.auth_scheme)])
async def get_list(service: Service = Depends(Service)):
    return await service.list()
