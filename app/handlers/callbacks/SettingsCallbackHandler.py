from aiogram import types

import app
from app.handlers import AbstractCallbackHandler
from app.handlers.commands.settings import NotificationSettingsCommandHandler
from app.helpers import UserHelper


class SettingsCallbackHandler(AbstractCallbackHandler):
    @staticmethod
    async def _update_user_notification_settings(
        callback_query: types.CallbackQuery, _row_name: str
    ):
        UserHelper.update_notification_settings(
            user_telegram_id=callback_query.from_user.id,
            setting_name=_row_name,
        )
        await NotificationSettingsCommandHandler.send_user_settings(
            user_id=callback_query.from_user.id, callback_query=callback_query
        )

    @staticmethod
    async def process(callback_query: types.CallbackQuery, *args, **kwargs):
        _row_name = callback_query.data.split('-')[1]
        if callback_query.data in ['notify_settings-discipline_sources']:
            return await app.bot.answer_callback_query(
                callback_query.id,
                text='Эта категория ещё недоступна.',
                show_alert=True,
            )
        if not UserHelper.is_user_orioks_authenticated(
            user_telegram_id=callback_query.from_user.id
        ):
            return await app.bot.answer_callback_query(
                callback_query.id,
                text='Нужно пройти авторизацию.',
                show_alert=True,
            )
        await SettingsCallbackHandler._update_user_notification_settings(
            callback_query, _row_name
        )
        await callback_query.answer()
