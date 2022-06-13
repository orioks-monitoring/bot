from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils import markdown

from config import Config

import db.user_first_add
import db.user_status


class UserOrioksAttemptsMiddleware(BaseMiddleware):
    """
        Middleware, блокирующее дальнейшее использование Бота,
        если превышено максимальное количество попыток входа в
        аккаунт ОРИОКС
    """

    # pylint: disable=unused-argument
    async def on_process_message(self, message: types.Message, *args, **kwargs):
        if db.user_status.get_user_orioks_attempts(
                user_telegram_id=message.from_user.id) > Config.ORIOKS_MAX_LOGIN_TRIES:
            await message.reply(
                markdown.text(
                    markdown.hbold('Ты совершил подозрительно много попыток входа в аккаунт ОРИОКС.'),
                    markdown.text('Возможно, ты нарушаешь <a href="https://orioks-monitoring.github.io/bot/rules">Пользовательское соглашение</a>, с которым согласился.'),
                    markdown.text(),
                    markdown.text('Связаться с поддержкой Бота: @orioks_monitoring_support'),
                    sep='\n',
                ),
                reply_markup=types.ReplyKeyboardRemove(),
                disable_web_page_preview=True,
            )
            raise CancelHandler()
