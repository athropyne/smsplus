import asyncio
import json

import starlette
from fastapi import Depends, HTTPException
from pydantic import ValidationError
from redis.asyncio import Redis
from starlette import status
from starlette.websockets import WebSocket

from celery_app.worker import notify
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
            # await message_transfer.connection.publish(f"message_to_{sender_id}", message_model.model_dump_json())
            return await self.repository.create(message_model.model_dump())  # сохранили в базе
        else:
            return await self._send_to_telegram(message_model)
            # asyncio.create_task(socket.send_text(output_model.model_dump_json()))  # отправляем себе
            # asyncio.create_task(
            #     socket.send_text(SENT_TO_TELEGRAM))  # отправляем системное себе
            # asyncio.create_task(self.repository.create(
            #     MessageModel(**model.model_dump(), signal=user_id).model_dump()))  # сохраняем в базу

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
        p = message_transfer.connection.pubsub()
        await p.subscribe(f"message_to_{user_id}")
        try:
            while True:
                message_model = None
                try:
                    # msg = await socket.receive_json()  # приняли сообщение
                    # print(msg)
                    # model = CreateModel(**msg)  # скрутили в класс модели, заодно отвалидировали
                    # receiver_socket = Online.get(
                    #     model.receiver)  # получили сокет получателя если он онлайн по ID из сообщения или None
                    # if receiver_socket is not None:  # если сокет есть
                    #     output_model = MessageModel(**model.model_dump(),
                    #                                 signal=user_id)  # скрутили в модель для отправки на сокет
                    #
                    #     asyncio.create_task(
                    #         receiver_socket.send_text(output_model.model_dump_json())),  # отправили чувачку
                    #     asyncio.create_task(socket.send_text(output_model.model_dump_json())),  # отправили себе
                    #     asyncio.create_task(self.repository.create(output_model.model_dump()))  # сохранили в базе
                    # else:  # если чувачок оффлайн
                    #     tg_ids = await self.helper.get_tg_id(model.receiver)  # пытаемся найти привязанные TelegramID
                    #     tg_ids = list(tg_ids)  # кучкуем результат в список
                    #     if len(tg_ids) == 0:  # если привязанной телеги нет
                    #         asyncio.create_task(socket.send_text(
                    #             system_messages.USER_NOT_AVAILABLE))  # отправляем себе системное сообщение о том что чувачок не найден нигде (может он даже не существует)
                    #
                    #     for tg_id in tg_ids:  # если TelegramID найдены 1 или больше (можно привязать несколько)
                    #         sender_login = await self.helper.convert_to_login(
                    #             user_id)  # конвертируем ID отправителя в логин
                    #         output_model = TelegramEventModel(**model.model_dump(),
                    #                                           signal=sender_login)  # скручиваем в модель для отправки в телегу
                    #         output_model.receiver = tg_id  # меняем ID чувачка на его TelegramID
                    #         result = notify.delay(output_model.model_dump_json())  # запускаем задачу на отправку
                    #         asyncio.create_task(socket.send_text(output_model.model_dump_json()))  # отправляем себе
                    #     asyncio.create_task(
                    #         socket.send_text(SENT_TO_TELEGRAM))  # отправляем системное себе
                    #     asyncio.create_task(self.repository.create(
                    #         MessageModel(**model.model_dump(), signal=user_id).model_dump()))  # сохраняем в базу
                    #

                    receiver_socket = Online.get(user_id)
                    msg = await p.get_message()
                    if msg:
                        print(msg)
                        if not isinstance(msg["data"], int):
                            message_model = MessageModel.parse_raw(msg["data"].decode())
                            # if receiver_socket:
                            await receiver_socket.send_text(message_model.model_dump_json())
                            continue
                            # else:

                            # sender_socket = Online.get(message_model.sender)
                            # if user_id == message_model.receiver:
                            #     await receiver_socket.send_text(message_model.model_dump_json())
                            # if user_id == message_model.sender:
                            #     await sender_socket.send_text(message_model.model_dump_json())
                        #     if receiver_socket:
                        #         print(1)
                        #         await receiver_socket.send_text(message_model.model_dump_json())
                        #     else:
                        #         print(2)
                        #         await self._send_to_telegram(message_model)
                        #         # if sender_socket:
                        #         #     await sender_socket.send_text(message_model.model_dump_json())
                        #         #     await sender_socket.send_text(
                        #         #         SystemMessage(signal="сообщение отправлено в телеграм").model_dump_json())
                        # if sender_socket:
                        #     print(3)
                        #     await sender_socket.send_text(message_model.model_dump_json())
                    await asyncio.sleep(2)
                    print("!!!")
                except json.decoder.JSONDecodeError:
                    await socket.send_json({"signal": "Невалидные данные"})
                    continue
                except ValidationError:
                    await socket.send_json({"signal": "Невалидные данные"})
                    continue
                except starlette.websockets.WebSocketDisconnect:
                    Online.remove(user_id)
                    if message_model:
                        result = await self._send_to_telegram(message_model)
                    break

        finally:
            Online.remove(user_id)

# class EventService:
#
#     def __init__(self,
#                  transfer: Redis = Depends(message_transfer),
#                  helper: Helper = Depends(Helper)):
#         self.transfer = transfer
#         self.helper = helper
