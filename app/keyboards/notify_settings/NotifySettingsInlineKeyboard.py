from aiogram import types

from app.helpers import UserHelper
from app.keyboards import AbstractInlineKeyboard
from app.models.users import UserNotifySettings
from config import config


class NotifySettingsInlineKeyboard(AbstractInlineKeyboard):
    @staticmethod
    def _get_section_name_with_status(
        attribute_name: str, is_on_off: UserNotifySettings
    ) -> str:
        emoji = '🔔' if getattr(is_on_off, attribute_name) else '❌'
        return (
            f'{emoji} {config.notify_settings_names_to_vars[attribute_name]}'
        )

    @staticmethod
    async def show(**kwargs) -> types.InlineKeyboardMarkup:
        """
        is_on_off = {
            'Обучение': False,
            'Новости': False,
            'Ресурсы': False,
            'Домашние задания': False,
            'Заявки': False,
        }
        """
        is_on_off = UserHelper.get_user_settings_by_telegram_id(
            kwargs.get('user_telegram_id')
        )

        inline_kb_full: types.InlineKeyboardMarkup = (
            types.InlineKeyboardMarkup(row_width=1)
        )
        inline_kb_full.add(
            types.InlineKeyboardButton(
                NotifySettingsInlineKeyboard._get_section_name_with_status(
                    'marks', is_on_off
                ),
                callback_data='notify_settings-marks',
            ),
            types.InlineKeyboardButton(
                NotifySettingsInlineKeyboard._get_section_name_with_status(
                    'news', is_on_off
                ),
                callback_data='notify_settings-news',
            ),
            types.InlineKeyboardButton(
                NotifySettingsInlineKeyboard._get_section_name_with_status(
                    'homeworks', is_on_off
                ),
                callback_data='notify_settings-homeworks',
            ),
            types.InlineKeyboardButton(
                NotifySettingsInlineKeyboard._get_section_name_with_status(
                    'requests', is_on_off
                ),
                callback_data='notify_settings-requests',
            ),
        )
        return inline_kb_full
