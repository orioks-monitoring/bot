from aiogram import types
from aiogram.utils import markdown

import keyboards
from app.handlers import AbstractCommandHandler

import db.user_status
import utils.handle_orioks_logout


class OrioksLogoutCommandHandler(AbstractCommandHandler):

    @staticmethod
    async def process(message: types.Message, *args, **kwargs):
        await message.reply(
            markdown.text(
                markdown.hbold('Выход из аккаунта ОРИОКС выполнен.'),
                markdown.text('Теперь ты НЕ будешь получать уведомления от Бота.'),
                sep='\n',
            ),
            reply_markup=keyboards.main_menu_keyboard(first_btn_text='Авторизация'),
        )
        db.user_status.update_user_orioks_authenticated_status(
            user_telegram_id=message.from_user.id,
            is_user_orioks_authenticated=False
        )
        utils.handle_orioks_logout.make_orioks_logout(user_telegram_id=message.from_user.id)
