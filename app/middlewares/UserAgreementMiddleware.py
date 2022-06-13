from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils import markdown

import db.user_first_add
import db.user_status


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

    async def on_process_message(self, message: types.Message, *args, **kwargs):
        db.user_first_add.user_first_add_to_db(user_telegram_id=message.from_user.id)
        if not db.user_status.get_user_agreement_status(user_telegram_id=message.from_user.id):
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
