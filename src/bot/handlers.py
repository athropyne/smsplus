import aiohttp
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import False_

from src.bot.states import Form

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("""Бот позволяет получать сообщения из чата когда вы в оффлайне. 
    Просто подпишитесь! Введите команду /subscribe , ввудите логин и пароль, указанные при регистрации.""")


@router.message(Command("subscribe"))
async def subscribe(message: Message, state: FSMContext):
    await message.answer("Введите свой логин")
    await state.set_state(Form.login)


@router.message(F.text, Form.login)
async def capture_login(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Введите свой пароль")
    await state.set_state(Form.password)


@router.message(F.text, Form.password)
async def capture_login(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    async with aiohttp.ClientSession() as session:
        token: str = ...
        async with session.post('http://localhost:8000/security/sign_in',
                                data=data) as resp:
            if resp.status == 200:
                result = await resp.json()
                token = result["access_token"]
        async with session.post("http://localhost:8000/security/bind_tg",
                                json=message.from_user.id,
                                headers={"Authorization":f"Bearer {token}"}) as resp:
            print(await resp.json())
    await state.clear()

