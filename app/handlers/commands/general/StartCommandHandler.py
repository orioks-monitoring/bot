from aiogram import types

from app.handlers import AbstractCommandHandler
from app.menus.start import StartMenu


class StartCommandHandler(AbstractCommandHandler):
    @staticmethod
    async def process(message: types.Message, *args, **kwargs) -> None:
        await StartMenu.show(
            chat_id=message.chat.id, telegram_user_id=message.from_user.id
        )
