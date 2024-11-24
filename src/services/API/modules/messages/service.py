import asyncio
import json

import redis.exceptions
import starlette
from fastapi import Depends, HTTPException, WebSocketException
from pydantic import ValidationError
from redis.asyncio import Redis
from redis.asyncio.client import PubSub
from sqlalchemy import ScalarResult
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
from modules.messages.utils import check_tg_ids, build_tg_event_model, is_online, is_online_user, build_message_model


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository),
                 transfer: Redis = Depends(message_transfer),
                 helper: Helper = Depends(Helper)):
        self.repository = repository
        self.transfer = transfer
        self.helper = helper

    async def _send_to_telegram(self, message_model: MessageModel):
        tg_ids = await self.helper.get_tg_ids(message_model.receiver)  # пытаемся найти привязанные TelegramID
        tg_ids = list(tg_ids)  # кучкуем результат в список
        check_tg_ids(tg_ids)
        for tg_id in tg_ids:  # если TelegramID найдены 1 или больше (можно привязать несколько)
            sender_login = await self.helper.convert_to_login(message_model.sender)  # конвертируем ID отправителя в логин
            output_model = build_tg_event_model(message_model.receiver,
                                                sender_login,
                                                message_model.text,
                                                message_model.created_at)  # скручиваем в модель для отправки в телегу
            output_model.receiver = tg_id  # меняем ID чувачка на его TelegramID
            result = notify.delay(output_model.model_dump_json())  # запускаем задачу на отправку
            return await self.repository.create(message_model.model_dump())  # сохранили в базе

    async def send(self, sender_id: int, receiver_id: int, text: str):
        if await is_online_user(receiver_id):
            message_model = build_message_model(sender_id, receiver_id, text)
            await message_transfer.connection.publish(
                f"message_to_{receiver_id}",
                message_model.model_dump_json())
            return await self.repository.create(message_model.model_dump())
        else:
            return await self._send_to_telegram(build_message_model(sender_id, receiver_id, text))

    async def get_history(self, self_id: int, interlocutor_id: int):
        """Возвращает историю сообщений"""
        return await self.repository.get_history(self_id, interlocutor_id)

