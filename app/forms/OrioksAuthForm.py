from aiogram.dispatcher.filters.state import State, StatesGroup


class OrioksAuthForm(StatesGroup):
    login = State()
    password = State()
