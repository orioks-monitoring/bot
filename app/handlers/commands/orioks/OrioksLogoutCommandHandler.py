from aiogram import types
from aiogram.utils import markdown

from app.handlers import AbstractCommandHandler

from app.helpers import OrioksHelper
from app.keyboards.authorization import AuthorizationReplyKeyboard


class OrioksLogoutCommandHandler(AbstractCommandHandler):
    @staticmethod
    async def process(message: types.Message, *args, **kwargs):
        user_telegram_id = message.from_user.id

        await message.reply(
            markdown.text(
                markdown.hbold('Выход из аккаунта ОРИОКС выполнен.'),
                markdown.text(
                    'Теперь ты НЕ будешь получать уведомления от Бота.'
                ),
                sep='\n',
            ),
            reply_markup=await AuthorizationReplyKeyboard.show(),
        )

        # UserHelper.update_authorization_status(user_telegram_id=user_telegram_id, is_authenticated=False)
        OrioksHelper.make_orioks_logout(user_telegram_id=user_telegram_id)
