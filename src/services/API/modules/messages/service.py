import asyncio
import json

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
from core.storages import message_transfer, Online
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
        receiver_socket = Online.get(receiver_id)
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

    def __check_token(self, token) -> int:
        try:
            return TokenManager.decode(token)
        except HTTPException:
            raise WebSocketException(code=status.WS_1002_PROTOCOL_ERROR,
                                     reason="доступ запрещен")

    async def __send_signal_for_kill_old_loop(self, user_id: int):
        """Посылает сигнал в старый цикл сообщений для его закрытия"""
        try:
            await message_transfer.connection.publish(f"signal_to_{user_id}",
                                                      SystemMessage(signal="stop").model_dump_json())
            logger.info("отправлен сигнал на закрытие старого цикла")

    async def __wait_competed_signal(self, p: PubSub, user_id: int):
        """Ждет пока придет сигнал о закрытии старого цикла"""
        while True:
            msg = await p.get_message()
            if msg:
                if not isinstance(msg["data"], int):
                    message_model = SystemMessage.parse_raw(msg["data"].decode())
                    if message_model.signal == "stopped":
                        print("получили сигнал подтверждения выхода")
                        break

    async def __send_completed_signal(self, user_id):
        """Отправляет сигнал о закрытии старого цикла"""
        await message_transfer.connection.publish(f"signal_to_{user_id}", SystemMessage(
            signal="stopped"
        ).model_dump_json())

    async def exchange(self,
                       socket: WebSocket):
        """Принимает сокет-подключения и ид пользователя, сохраняя их в словарь онлайн пользователей.
        Осуществляет прием и отправку сообщений. (Все одной большой функцией для удобства отладки.)"""
        # token = await socket.receive_text()
        # user_id = self.__check_token(token)

        user_id = 1
        p = message_transfer.connection.pubsub()
        if user_id in Online.users:
            await self.__send_signal_for_kill_old_loop(user_id)
            await p.subscribe(f"signal_to_{user_id}")
            await self.__wait_competed_signal(p, user_id)
            await p.unsubscribe(f"signal_to_{user_id}")

        await socket.accept()
        Online.add(user_id, socket)
        await socket.send_text(SystemMessage(signal="доступ разрешен").model_dump_json())
        await p.subscribe(f"message_to_{user_id}", f"signal_to_{user_id}")
        try:
            while True:
                message_model = None
                try:
                    receiver_socket = Online.get(user_id)
                    msg = await p.get_message()
                    print(Online.users)
                    if msg:
                        print(msg)
                        if not isinstance(msg["data"], int):
                            if msg["channel"].decode() == f"signal_to_{user_id}":
                                message_model = SystemMessage.parse_raw(msg["data"].decode())
                                if message_model.signal == "stop":
                                    await socket.close()
                                    Online.remove(user_id)
                                    await self.__send_completed_signal(user_id)
                                    await p.unsubscribe(f"message_to_{user_id}", f"signal_to_{user_id}")
                                    break
                            message_model = MessageModel.parse_raw(msg["data"].decode())

                            print(f"message_model {message_model}")
                            await receiver_socket.send_text(message_model.model_dump_json())
                            continue
                    await receiver_socket.send_text(SystemMessage(signal="ping").model_dump_json())
                    await asyncio.sleep(2)
                except json.decoder.JSONDecodeError:
                    await socket.send_json({"signal": "Невалидные данные"})
                    continue
                except ValidationError:
                    await socket.send_json({"signal": "Невалидные данные"})
                    continue
                except starlette.websockets.WebSocketDisconnect:
                    Online.remove(user_id)
                    await message_transfer.connection.close()
                    if message_model:
                        result = await self._send_to_telegram(message_model)
                    break
            print("пока еще в цикле")
        finally:

            print("выходим")
            print(f"в онлайне остались {Online.users}")
        print("ушел")

# class EventService:
#
#     def __init__(self,
#                  transfer: Redis = Depends(message_transfer),
#                  helper: Helper = Depends(Helper)):
#         self.transfer = transfer
#         self.helper = helper
