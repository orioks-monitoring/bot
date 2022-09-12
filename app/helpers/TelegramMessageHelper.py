import pathlib

from aiogram.types import InputFile
from aiogram.utils import markdown
from aiogram.utils.exceptions import BotBlocked, ChatNotFound

import app
from app.helpers import OrioksHelper
from config import config


class TelegramMessageHelper:
    @staticmethod
    async def text_message_to_user(
        user_telegram_id: int, message: str
    ) -> None:
        try:
            await app.bot.send_message(user_telegram_id, message)
        except (BotBlocked, ChatNotFound):
            OrioksHelper.make_orioks_logout(user_telegram_id=user_telegram_id)

    @staticmethod
    async def photo_message_to_user(
        user_telegram_id: int, photo_path: pathlib.Path, caption: str
    ) -> None:
        try:
            await app.bot.send_photo(
                user_telegram_id, InputFile(photo_path), caption
            )
        except (BotBlocked, ChatNotFound):
            OrioksHelper.make_orioks_logout(user_telegram_id=user_telegram_id)

    @staticmethod
    async def message_to_admins(message: str) -> None:
        for admin_telegram_id in config.TELEGRAM_ADMIN_IDS_LIST:
            await app.bot.send_message(
                admin_telegram_id,
                markdown.text(
                    markdown.hbold('[ADMIN]'),
                    markdown.text(message),
                    sep=': ',
                ),
            )
