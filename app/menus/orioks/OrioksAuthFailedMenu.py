from aiogram.utils import markdown

import app
from app.keyboards.authorization import AuthorizationReplyKeyboard
from app.helpers import UserHelper
from app.menus.AbstractMenu import AbstractMenu


class OrioksAuthFailedMenu(AbstractMenu):

    @staticmethod
    async def show(chat_id: int, telegram_user_id: int) -> None:
        if not UserHelper.is_user_orioks_authenticated(user_telegram_id=telegram_user_id):
            await app.bot.send_message(
                chat_id,
                markdown.text(
                    markdown.hbold('Ошибка авторизации!'),
                    markdown.text('Попробуйте ещё раз: /login'),
                    sep='\n',
                ),
                reply_markup=await AuthorizationReplyKeyboard.show(),
            )
