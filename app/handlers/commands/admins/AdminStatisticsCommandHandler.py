from aiogram import types
from aiogram.utils import markdown

from app.handlers import AbstractCommandHandler

import db.admins_statistics
from app.handlers.commands.settings import NotificationSettingsCommandHandler
from config import Config


class AdminStatisticsCommandHandler(AbstractCommandHandler):

    @staticmethod
    async def process(message: types.Message, *args, **kwargs):
        msg = ''
        for key, value in db.admins_statistics.select_count_user_status_statistics().items():
            msg += markdown.text(
                markdown.text(key),
                markdown.text(value),
                sep=': ',
            ) + '\n'
        msg += '\n'

        for category in ('marks', 'news', 'discipline_sources', 'homeworks', 'requests'):
            msg += markdown.text(
                markdown.text(NotificationSettingsCommandHandler.notify_settings_names_to_vars[category]),
                markdown.text(db.admins_statistics.select_count_notify_settings_row_name(row_name=category)),
                sep=': ',
            ) + '\n'
        msg += '\n'

        for key, value in db.admins_statistics.select_all_from_admins_statistics().items():
            msg += markdown.text(
                markdown.text(key),
                markdown.text(value),
                sep=': ',
            ) + '\n'

        requests_wave_time = (
                 db.admins_statistics.select_count_notify_settings_row_name(row_name='marks') +
                 2 +  # marks category
                 db.admins_statistics.select_count_notify_settings_row_name(
                     row_name='discipline_sources') +
                 db.admins_statistics.select_count_notify_settings_row_name(row_name='homeworks') +
                 db.admins_statistics.select_count_notify_settings_row_name(row_name='requests') * 3
         ) * Config.ORIOKS_SECONDS_BETWEEN_REQUESTS / 60
        msg += markdown.text(
            markdown.text('Примерное время выполнения одной волны запросов'),
            markdown.text(
                markdown.text(round(requests_wave_time, 2)),
                markdown.text('минут'),
                sep=' ',
            ),
            sep=': ',
        ) + '\n'
        await message.reply(msg)
