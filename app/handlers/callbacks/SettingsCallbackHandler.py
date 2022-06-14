from aiogram import types

import app
import db.notify_settings
from app.handlers import AbstractCallbackHandler
from app.handlers.commands.settings import NotificationSettingsCommandHandler


class SettingsCallbackHandler(AbstractCallbackHandler):

    @staticmethod
    async def process(callback_query: types.CallbackQuery, *args, **kwargs):
        _row_name = callback_query.data.split('-')[1]
        if callback_query.data in ['notify_settings-discipline_sources']:
            return await app.bot.answer_callback_query(
                callback_query.id,
                text='Эта категория ещё недоступна.', show_alert=True
            )
        db.notify_settings.update_user_notify_settings(
            user_telegram_id=callback_query.from_user.id,
            row_name=_row_name,
            to_value=not db.notify_settings.get_user_notify_settings_to_dict(
                user_telegram_id=callback_query.from_user.id)[_row_name],
        )
        await NotificationSettingsCommandHandler.send_user_settings(
            user_id=callback_query.from_user.id, callback_query=callback_query
        )
