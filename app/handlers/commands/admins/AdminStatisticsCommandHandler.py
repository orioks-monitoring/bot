from aiogram import types
from aiogram.utils import markdown

from app.handlers import AbstractCommandHandler

from app.helpers import AdminHelper
from config import config


class AdminStatisticsCommandHandler(AbstractCommandHandler):
    @staticmethod
    async def process(message: types.Message, *args, **kwargs):
        msg = ''
        for key, value in AdminHelper.get_count_users_statistics().items():
            msg += (
                markdown.text(
                    markdown.text(key),
                    markdown.text(value),
                    sep=': ',
                )
                + '\n'
            )
        msg += '\n'

        for category in (
            'marks',
            'news',
            'homeworks',
            'requests',
        ):
            msg += (
                markdown.text(
                    markdown.text(
                        config.notify_settings_names_to_vars[category]
                    ),
                    markdown.text(
                        AdminHelper.get_count_notify_settings_by_row_name(
                            row_name=category
                        )
                    ),
                    sep=': ',
                )
                + '\n'
            )
        msg += '\n'

        for key, value in AdminHelper.get_general_statistics().items():
            msg += (
                markdown.text(
                    markdown.text(key),
                    markdown.text(value),
                    sep=': ',
                )
                + '\n'
            )

        requests_wave_time = (
            (
                AdminHelper.get_count_notify_settings_by_row_name(
                    row_name='marks'
                )
                + 2
                + AdminHelper.get_count_notify_settings_by_row_name(
                    row_name='homeworks'
                )
                + AdminHelper.get_count_notify_settings_by_row_name(
                    row_name='requests'
                )
                * 3
            )
            * config.ORIOKS_SECONDS_BETWEEN_REQUESTS
            / 60
        )
        msg += (
            markdown.text(
                markdown.text(
                    'Примерное время выполнения одной волны запросов'
                ),
                markdown.text(
                    markdown.text(round(requests_wave_time, 2)),
                    markdown.text('минут'),
                    sep=' ',
                ),
                sep=': ',
            )
            + '\n'
        )
        await message.reply(msg)
