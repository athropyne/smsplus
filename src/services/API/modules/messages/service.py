import asyncio
import json

import redis.exceptions
import starlette
from fastapi import Depends, HTTPException, WebSocketException
from pydantic import ValidationError
from redis.asyncio import Redis
from redis.asyncio.client import PubSub
from starlette import status
from starlette.websockets import WebSocket

from celery_app.worker import notify
from core.config import logger
from core.security import TokenManager
from core.storages import message_transfer, Online, online_user_storage
# from modules.messages import system_messages
from modules.messages.dto import MessageModel, TelegramEventModel, SystemMessage
from modules.messages.helpers import Helper
from modules.messages.repository import Repository


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository),
                 transfer: Redis = Depends(message_transfer),
                 helper: Helper = Depends(Helper)):
        self.repository = repository
        self.transfer = transfer
        self.helper = helper

    async def _send_to_telegram(self, message_model: MessageModel):
        tg_ids = await self.helper.get_tg_id(message_model.receiver)  # пытаемся найти привязанные TelegramID
        tg_ids = list(tg_ids)  # кучкуем результат в список
        if len(tg_ids) == 0:  # если привязанной телеги нет
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь не в сети и не подписан на уведомления. Сообщение не отправлено"
            )  # отправляем себе системное сообщение о том что чувачок не найден нигде (может он даже не существует)

        for tg_id in tg_ids:  # если TelegramID найдены 1 или больше (можно привязать несколько)
            sender_login = await self.helper.convert_to_login(
                message_model.sender)  # конвертируем ID отправителя в логин
            output_model = TelegramEventModel(
                receiver=message_model.receiver,
                sender=sender_login,
                text=message_model.text,
                created_at=message_model.created_at)  # скручиваем в модель для отправки в телегу
            output_model.receiver = tg_id  # меняем ID чувачка на его TelegramID
            result = notify.delay(output_model.model_dump_json())  # запускаем задачу на отправку
            return await self.repository.create(message_model.model_dump())  # сохранили в базе

    async def send(self, sender_id: int, receiver_id: int, text: str):
        async with online_user_storage as connection:
            receiver_socket = await connection.get(receiver_id)
        message_model = MessageModel(
            sender=sender_id,
            receiver=receiver_id,
            text=text
        )
        if receiver_socket:
            await message_transfer.connection.publish(f"message_to_{receiver_id}", message_model.model_dump_json())
            return await self.repository.create(message_model.model_dump())  # сохранили в базе
        else:
            return await self._send_to_telegram(message_model)

    async def get_history(self, self_id: int, interlocutor_id: int):
        """Возвращает историю сообщений"""
        return await self.repository.get_history(self_id, interlocutor_id)

