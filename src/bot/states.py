from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    login = State()
    password = State()
