from aiogram import types
from aiogram.utils import markdown

from app.handlers import AbstractCommandHandler

from app.helpers import LoginLogoutHelper
from app.keyboards.authorization import AuthorizationReplyKeyboard


class OrioksLogoutCommandHandler(AbstractCommandHandler):
    @staticmethod
    async def process(message: types.Message, *args, **kwargs):
        user_telegram_id = message.from_user.id

        await LoginLogoutHelper.make_logout(user_telegram_id)
        await message.reply(
            markdown.text(
                markdown.hbold("Выход из аккаунта ОРИОКС выполнен."),
                markdown.text("Теперь ты НЕ будешь получать уведомления от Бота."),
                sep="\n",
            ),
            reply_markup=await AuthorizationReplyKeyboard.show(),
        )
