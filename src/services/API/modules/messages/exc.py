from fastapi import HTTPException
from starlette import status


class UserIsNotAvailable(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь не в сети и не подписан на уведомления. Сообщение не отправлено"
        )
