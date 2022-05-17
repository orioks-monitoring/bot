from aiogram import types
import aiogram.utils.markdown as md

import config
import handlers.notify_settings
import db.admins_statistics
import db.notify_settings


async def admin_get_statistics(message: types.Message):
    msg = ''
    for key, value in db.admins_statistics.select_count_user_status_statistics().items():
        msg += md.text(
            md.text(key),
            md.text(value),
            sep=': ',
        ) + '\n'
    msg += '\n'

    for category in ('marks', 'news', 'discipline_sources', 'homeworks', 'requests'):
        msg += md.text(
            md.text(handlers.notify_settings.notify_settings_names_to_vars[category]),
            md.text(db.admins_statistics.select_count_notify_settings_row_name(row_name=category)),
            sep=': ',
        ) + '\n'
    msg += '\n'

    for key, value in db.admins_statistics.select_all_from_admins_statistics().items():
        msg += md.text(
            md.text(key),
            md.text(value),
            sep=': ',
        ) + '\n'

    requests_wave_time = (
                             db.admins_statistics.select_count_notify_settings_row_name(row_name='marks') +
                             2 +  # marks category
                             db.admins_statistics.select_count_notify_settings_row_name(row_name='discipline_sources') +
                             db.admins_statistics.select_count_notify_settings_row_name(row_name='homeworks') +
                             db.admins_statistics.select_count_notify_settings_row_name(row_name='requests') * 3
                         ) * config.ORIOKS_SECONDS_BETWEEN_REQUESTS / 60
    msg += md.text(
        md.text('Примерное время выполнения одной волны запросов'),
        md.text(
            md.text(round(requests_wave_time, 2)),
            md.text('минут'),
            sep=' ',
        ),
        sep=': ',
    ) + '\n'
    await message.reply(msg)
