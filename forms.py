from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    login = State()
    password = State()
