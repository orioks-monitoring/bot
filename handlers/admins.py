from aiogram import types
import aiogram.utils.markdown as md

import handlers.notify_settings
import db
import logging

logger = logging.getLogger(__name__)


async def admin_get_statistics(message: types.Message):
    msg = ""
    for key, value in db.select_count_user_status_statistics().items():
        msg += f'{key}: {value}\n'
    msg += '\n'
    for key, value in db.select_count_notify_settings_statistics().items():
        msg += f'{handlers.notify_settings.notify_settings_names_to_vars[key]}: {value}\n'

    await message.reply(
        md.text(
            md.text(msg),
        )
    )
