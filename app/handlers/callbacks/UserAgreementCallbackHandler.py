from aiogram import types
import app
from app.handlers import AbstractCallbackHandler
from app.helpers import UserHelper
from app.menus.start import StartMenu


class UserAgreementCallbackHandler(AbstractCallbackHandler):

    @staticmethod
    async def process(callback_query: types.CallbackQuery, *args, **kwargs):
        user_telegram_id = callback_query.from_user.id

        if UserHelper.is_user_agreement_accepted(user_telegram_id=user_telegram_id):
            return await app.bot.answer_callback_query(
                callback_query.id,
                text='Пользовательское соглашение уже принято.', show_alert=True)

        UserHelper.accept_user_agreement(user_telegram_id=user_telegram_id)

        await app.bot.answer_callback_query(callback_query.id)
        answer_message = await app.bot.send_message(user_telegram_id, 'Пользовательское соглашение принято!')
        await StartMenu.show(chat_id=answer_message.chat.id, telegram_user_id=user_telegram_id)
