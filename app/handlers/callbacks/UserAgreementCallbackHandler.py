from aiogram import types
import db.user_status
import app
from app.handlers import AbstractCallbackHandler
from app.menus.start import StartMenu


class UserAgreementCallbackHandler(AbstractCallbackHandler):

    @staticmethod
    async def process(callback_query: types.CallbackQuery, *args, **kwargs):
        if db.user_status.get_user_agreement_status(user_telegram_id=callback_query.from_user.id):
            return await app.bot.answer_callback_query(
                callback_query.id,
                text='Пользовательское соглашение уже принято.', show_alert=True)
        db.user_status.update_user_agreement_status(
            user_telegram_id=callback_query.from_user.id,
            is_user_agreement_accepted=True
        )
        await app.bot.answer_callback_query(callback_query.id)
        answer_message = await app.bot.send_message(callback_query.from_user.id, 'Пользовательское соглашение принято!')
        await StartMenu.show(chat_id=answer_message.chat.id, telegram_user_id=callback_query.from_user.id)
