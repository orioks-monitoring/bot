from aiogram import types
from aiogram.utils import markdown

import app
from app.handlers import AbstractCommandHandler
from app.helpers import UserHelper
from app.models.users import UserNotifySettings


class NotificationSettingsCommandHandler(AbstractCommandHandler):

    notify_settings_names_to_vars = {
        'marks': 'Оценки',
        'news': 'Новости',
        'discipline_sources': 'Ресурсы',
        'homeworks': 'Домашние задания',
        'requests': 'Заявки',
    }

    @staticmethod
    def _get_section_name_with_status(attribute_name: str, is_on_off: UserNotifySettings) -> str:
        emoji = '🔔' if getattr(is_on_off, attribute_name) else '❌'
        return f'{emoji} {NotificationSettingsCommandHandler.notify_settings_names_to_vars[attribute_name]}'

    @staticmethod
    def init_notify_settings_inline_btns(is_on_off: dict) -> types.InlineKeyboardMarkup:
        """
        is_on_off = {
            'Обучение': False,
            'Новости': False,
            'Ресурсы': False,
            'Домашние задания': False,
            'Заявки': False,
        }
        """
        inline_kb_full: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup(row_width=1)
        inline_kb_full.add(
            types.InlineKeyboardButton(
                NotificationSettingsCommandHandler._get_section_name_with_status('marks', is_on_off),
                callback_data='notify_settings-marks'
            ),
            types.InlineKeyboardButton(
                NotificationSettingsCommandHandler._get_section_name_with_status('news', is_on_off),
                callback_data='notify_settings-news'
            ),
            types.InlineKeyboardButton(
                NotificationSettingsCommandHandler._get_section_name_with_status('discipline_sources', is_on_off),
                callback_data='notify_settings-discipline_sources'
            ),
            types.InlineKeyboardButton(
                NotificationSettingsCommandHandler._get_section_name_with_status('homeworks', is_on_off),
                callback_data='notify_settings-homeworks'
            ),
            types.InlineKeyboardButton(
                NotificationSettingsCommandHandler._get_section_name_with_status('requests', is_on_off),
                callback_data='notify_settings-requests'
            )
        )
        return inline_kb_full

    @staticmethod
    async def process(message: types.Message, *args, **kwargs):
        await NotificationSettingsCommandHandler.send_user_settings(message.from_user.id, callback_query=None)

    @staticmethod
    async def send_user_settings(user_id: int, callback_query: types.CallbackQuery = None) -> types.Message:
        is_on_off_dict = UserHelper.get_user_settings_by_telegram_id(user_telegram_id=user_id)
        text = markdown.text(
            markdown.text(
                markdown.text('📓'),
                markdown.text(
                    markdown.hbold('“Обучение”'),
                    markdown.text('изменения баллов в накопительно-балльной системе (НБС)'),
                    sep=': ',
                ),
                sep=' ',
            ),
            markdown.text(
                markdown.text('📰'),
                markdown.text(
                    markdown.hbold('“Новости”'),
                    markdown.text('публикация общих новостей\n(новости по дисциплинам', markdown.hitalic('(coming soon))')),
                    sep=': ',
                ),
                sep=' ',
            ),
            markdown.text(
                markdown.text('📁'),
                markdown.text(
                    markdown.hbold('“Ресурсы”'),
                    markdown.text('изменения и загрузка файлов по дисциплине', markdown.hitalic('(coming soon)')),
                    sep=': ',
                ),
                sep=' ',
            ),
            markdown.text(
                markdown.text('📝'),
                markdown.text(
                    markdown.hbold('“Домашние задания”'),
                    markdown.text('изменения статусов отправленных работ'),
                    sep=': ',
                ),
                sep=' ',
            ),
            markdown.text(
                markdown.text('📄'),
                markdown.text(
                    markdown.hbold('“Заявки”'),
                    markdown.text('изменения статусов заявок на обходной лист, материальную помощь, '
                                  'социальную стипендию, копии документов, справки'),
                    sep=': ',
                ),
                sep=' ',
            ),
            sep='\n\n',
        )
        if not callback_query:
            return await app.bot.send_message(
                user_id,
                text=text,
                reply_markup=NotificationSettingsCommandHandler.init_notify_settings_inline_btns(
                    is_on_off=is_on_off_dict
                ),
            )
        return await callback_query.message.edit_text(
            text=text,
            reply_markup=NotificationSettingsCommandHandler.init_notify_settings_inline_btns(
                is_on_off=is_on_off_dict
            ),
        )
