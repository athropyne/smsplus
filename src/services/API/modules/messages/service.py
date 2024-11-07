import asyncio
import json

import starlette
from fastapi import Depends
from pydantic import ValidationError
from redis.asyncio import Redis
from starlette.websockets import WebSocket

from modules.messages import system_messages
from modules.messages.dto import CreateModel, MessageModel, SystemMessage, TelegramEventModel
from modules.messages.helpers import Helper
from modules.messages.repository import Repository
from celery_app.worker import notify
from core.storages import message_transfer, Online


class Service:
    def __init__(self,
                 repository: Repository = Depends(Repository),
                 transfer: Redis = Depends(message_transfer),
                 helper: Helper = Depends(Helper)):
        self.repository = repository
        self.transfer = transfer
        self.helper = helper

    async def get_history(self, self_id: int, interlocutor_id: int):
        """Возвращает историю сообщений"""
        return await self.repository.get_history(self_id, interlocutor_id)

    async def exchange(self,
                       user_id: int,
                       socket: WebSocket):
        """Принимает сокет-подключения и ид пользователя, сохраняя их в словарь онлайн пользователей.
        Осуществляет прием и отправку сообщений. (Все одной большой функцией для удобства отладки.)"""
        await socket.accept()
        Online.add(user_id, socket)
        try:
            while True:
                try:
                    msg = await socket.receive_json()  # приняли сообщение
                    model = CreateModel(**msg)  # скрутили в класс модели, заодно отвалидировали
                    receiver_socket = Online.get(
                        model.receiver)  # получили сокет получателя если он онлайн по ID из сообщения или None
                    if receiver_socket is not None:  # если сокет есть
                        output_model = MessageModel(**model.model_dump(),
                                                    sender=user_id)  # скрутили в модель для отправки на сокет
                        await asyncio.gather(*[
                            asyncio.create_task(receiver_socket.send_text(output_model.model_dump_json())), # отправили чувачку
                            asyncio.create_task(socket.send_text(output_model.model_dump_json())),  # отправили себе
                            asyncio.create_task(self.repository.create(output_model.model_dump())) # сохранили в базе
                        ])
                    else:  # если чувачок не оффлайн
                        tg_ids = await self.helper.get_tg_id(model.receiver)  # пытаемся найти привязанные TelegramID
                        tg_ids = list(tg_ids)  # кучкуем результат в список
                        if len(tg_ids) == 0:  # если привязанной телеги нет
                            asyncio.create_task(socket.send_text(
                                system_messages.USER_NOT_AVAILABLE))  # отправляем себе системное сообщение о том что чувачок не найден нигде (может он даже не существует)
                        tasks = []
                        for tg_id in tg_ids:  # если TelegramID найдены 1 или больше (можно привязать несколько)
                            sender_login = await self.helper.convert_to_login(
                                user_id)  # конвертируем ID отправителя в логин
                            output_model = TelegramEventModel(**model.model_dump(),
                                                              sender=sender_login)  # скручиваем в модель для отправки в телегу
                            output_model.receiver = tg_id  # меняем ID чувачка на его TelegramID
                            result = notify.delay(tg_id, output_model.model_dump_json())  # запускаем задачу на отправку
                            tasks.append(asyncio.create_task(socket.send_text(output_model.model_dump_json())))  # отправляем себе
                        tasks.append(asyncio.create_task(socket.send_text(SystemMessage().model_dump_json())))  # отправляем системное себе
                        tasks.append(asyncio.create_task(self.repository.create(MessageModel(**model.model_dump(), sender=user_id).model_dump())))  # сохраняем в базу
                        await asyncio.gather(*tasks)

                except json.decoder.JSONDecodeError:
                    await socket.send_text(system_messages.INCORRECT_DATA)
                    continue
                except ValidationError:
                    await socket.send_text(system_messages.INCORRECT_DATA)
                    continue
        except starlette.websockets.WebSocketDisconnect:
            return "пользователь отключен"
        finally:
            Online.remove(user_id)

# class EventService:
#
#     def __init__(self,
#                  transfer: Redis = Depends(message_transfer),
#                  helper: Helper = Depends(Helper)):
#         self.transfer = transfer
#         self.helper = helper
