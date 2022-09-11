from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils import markdown

from app.helpers import UserHelper


class UserAgreementMiddleware(BaseMiddleware):
    """
        Middleware, блокирующее дальнейшее использование Бота,
        если не принято пользовательское соглашение
    """

    inline_btn_user_agreement_accept = types.InlineKeyboardButton(
        'Принять пользовательское соглашение',
        callback_data='button_user_agreement_accept'
    )
    inline_agreement_accept = types.InlineKeyboardMarkup().add(inline_btn_user_agreement_accept)

    # pylint: disable=unused-argument
    async def on_process_message(self, message: types.Message, *args, **kwargs):
        user_telegram_id = message.from_user.id
        UserHelper.create_user_if_not_exist(user_telegram_id=user_telegram_id)
        if not UserHelper.is_user_agreement_accepted(user_telegram_id=user_telegram_id):
            await message.reply(
                markdown.text(
                    markdown.text('Для получения доступа к Боту, необходимо принять Пользовательское соглашение:'),
                    markdown.text('https://orioks-monitoring.github.io/bot/rules'),
                    sep='\n',
                ),
                reply_markup=self.inline_agreement_accept,
                disable_web_page_preview=True,
            )
            raise CancelHandler()
