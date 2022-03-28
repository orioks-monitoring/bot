from aiogram import types
import aiogram.utils.markdown as md

import handlers.notify_settings
import db.admins_statistics
import db.user_status
import db.notify_settings


async def admin_get_statistics(message: types.Message):
    msg = ''
    for key, value in db.user_status.select_count_user_status_statistics().items():
        msg += md.text(
            md.text(key),
            md.text(value),
            sep=': ',
        ) + '\n'
    msg += '\n'
    for key, value in db.notify_settings.select_count_notify_settings_statistics().items():
        msg += md.text(
            md.text(handlers.notify_settings.notify_settings_names_to_vars[key]),
            md.text(value),
            sep=': ',
        ) + '\n'
    msg += '\n'
    for key, value in db.admins_statistics.select_all_from_admins_statistics().items():
        msg += md.text(
            md.text(key),
            md.text(value),
            sep=': ',
        ) + '\n'

    await message.reply(msg)
