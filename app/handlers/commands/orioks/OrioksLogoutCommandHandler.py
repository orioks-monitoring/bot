from aiogram import types
from aiogram.utils import markdown

import keyboards
from app.handlers import AbstractCommandHandler

from app.helpers import OrioksHelper


class OrioksLogoutCommandHandler(AbstractCommandHandler):

    @staticmethod
    async def process(message: types.Message, *args, **kwargs):
        user_telegram_id = message.from_user.id

        await message.reply(
            markdown.text(
                markdown.hbold('Выход из аккаунта ОРИОКС выполнен.'),
                markdown.text('Теперь ты НЕ будешь получать уведомления от Бота.'),
                sep='\n',
            ),
            reply_markup=keyboards.main_menu_keyboard(first_btn_text='Авторизация'),
        )

        # UserHelper.update_authorization_status(user_telegram_id=user_telegram_id, is_authenticated=False)
        OrioksHelper.make_orioks_logout(user_telegram_id=user_telegram_id)
