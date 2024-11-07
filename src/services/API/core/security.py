import datetime
from datetime import timedelta, timezone

import jwt
import passlib.context
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.requests import Request
from starlette.websockets import WebSocket

from core import config


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request = None, websocket: WebSocket = None):
        return await super().__call__(request or websocket)


auth_scheme = CustomOAuth2PasswordBearer(tokenUrl="security/sign_in")


class PasswordManager:
    _context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password: str) -> str:
        return cls._context.hash(password)

    @classmethod
    def verify(cls, plain: str, hashed_str: str) -> bool:
        return cls._context.verify(plain, hashed_str)


class TokenManager:
    _ALGORITHM = "HS256"
    _TOKEN_SECRET_KEY = config.TOKEN_SECRET_KEY()
    _ACCESS_TOKEN_EXPIRE_SECOND = config.ACCESS_TOKEN_EXPIRE_MINUTES()

    @classmethod
    def create(cls, data: dict, expire_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.datetime.now(tz=timezone.utc) + expire_delta
        to_encode.update({"exp": expire})
        try:
            jwt_str = jwt.encode(to_encode, cls._TOKEN_SECRET_KEY, cls._ALGORITHM)
            return jwt_str
        except:
            print("token not created!")

    @classmethod
    def decode(cls, token: str = Depends(auth_scheme)) -> int:
        try:
            payload: dict = jwt.decode(token, cls._TOKEN_SECRET_KEY, cls._ALGORITHM)
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            return int(user_id)
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
