import logging

from aiogram import types

from answers import settings

logger = logging.getLogger(__name__)

notify_settings_names_to_vars = {
    'marks': 'Оценки',
    'news': 'Новости',
    'discipline_sources': 'Ресурсы',
    'homeworks': 'Домашние задания',
    'requests': 'Заявки',
}


def _get_section_name_with_status(section_name: str, is_on_off: dict) -> str:
    emoji = '🔔' if is_on_off[section_name] else '❌'
    return f'{emoji} {notify_settings_names_to_vars[section_name]}'


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
        types.InlineKeyboardButton(_get_section_name_with_status('marks', is_on_off),
                                   callback_data='notify_settings-marks'),
        types.InlineKeyboardButton(_get_section_name_with_status('news', is_on_off),
                                   callback_data='notify_settings-news'),
        types.InlineKeyboardButton(_get_section_name_with_status('discipline_sources', is_on_off),
                                   callback_data='notify_settings-discipline_sources'),
        types.InlineKeyboardButton(_get_section_name_with_status('homeworks', is_on_off),
                                   callback_data='notify_settings-homeworks'),
        types.InlineKeyboardButton(_get_section_name_with_status('requests', is_on_off),
                                   callback_data='notify_settings-requests')
    )
    return inline_kb_full


async def user_settings(message: types.Message):
    await settings.send_user_settings(user_id=message.from_user.id)
