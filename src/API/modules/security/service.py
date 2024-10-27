from fastapi import Depends, HTTPException
from starlette import status

from src.core.security import PasswordManager, TokenManager
from src.API.modules.security.repository import Repository


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository)):
        self.repository = repository

    async def sign_in(self, login: str, password: str):
        user = await self.repository.get_by_login(login)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="user not found")

        if not PasswordManager.verify(password, user["password"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="invalid login or password")

        token = TokenManager.create({"sub": user["id"]})
        return {"access_token": token, "token_type": "bearer"}

    async def bind_tg(self, user_id: int, tg_id: int):
        return await self.repository.bind_tg(user_id, tg_id)
