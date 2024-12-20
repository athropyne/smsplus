from fastapi import HTTPException
from starlette import status


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="invalid login or password")


class InvalidPassword(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="invalid login or password")
