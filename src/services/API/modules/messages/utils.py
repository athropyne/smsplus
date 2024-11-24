import datetime
from typing import List

from core.storages import online_user_storage
from modules.messages.dto import TelegramEventModel, MessageModel
from modules.messages.exc import UserIsNotAvailable


def check_tg_ids(tg_ids: List[int]):
    if len(tg_ids) == 0:  # если привязанной телеги нет
        raise UserIsNotAvailable


def build_tg_event_model(receiver: int,
                         sender_login: str,
                         text: str,
                         created_at: datetime.datetime):
    return TelegramEventModel(
        receiver=receiver,
        sender=sender_login,
        text=text,
        created_at=created_at)  # скручиваем в модель для отправки в телегу


async def is_online_user(receiver_id: int) -> bool:
    async with online_user_storage as connection:
        receiver_socket = await connection.get(receiver_id)
    return True if receiver_socket else False


def build_message_model(sender_id: int, receiver_id: int, text: str):
    return MessageModel(
        sender=sender_id,
        receiver=receiver_id,
        text=text
    )
