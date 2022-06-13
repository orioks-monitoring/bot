from aiogram.utils import markdown

import app
import keyboards
from app.menus.AbstractMenu import AbstractMenu

import db.user_status


class OrioksAuthFailedMenu(AbstractMenu):

    @staticmethod
    async def show(chat_id: int, telegram_user_id: int) -> None:
        if not db.user_status.get_user_orioks_authenticated_status(user_telegram_id=telegram_user_id):
            await app.bot.send_message(
                chat_id,
                markdown.text(
                    markdown.hbold('Ошибка авторизации!'),
                    markdown.text('Попробуйте ещё раз: /login'),
                    sep='\n',
                ),
                reply_markup=keyboards.main_menu_keyboard(first_btn_text='Авторизация')
            )
