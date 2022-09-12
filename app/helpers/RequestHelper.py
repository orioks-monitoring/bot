import asyncio
import logging

import aiohttp

from app.helpers import AdminHelper
from config import config


class RequestHelper:
    _sem = asyncio.Semaphore(config.ORIOKS_REQUESTS_SEMAPHORE_VALUE)

    @staticmethod
    async def get_request(url: str, session: aiohttp.ClientSession) -> str:
        async with RequestHelper._sem:  # next coroutine(s) will stuck here until the previous is done
            await asyncio.sleep(
                config.ORIOKS_SECONDS_BETWEEN_REQUESTS
            )  # orioks dont die please
            # TODO: is db.user_status.get_user_orioks_authenticated_status(user_telegram_id=user_telegram_id)
            #       else safe delete all user's file
            #       Обработать случай, когда пользователь к моменту достижения своей очереди разлогинился
            # TODO: is db.notify_settings.get_user_notify_settings_to_dict(user_telegram_id=user_telegram_id)
            #       else safe delete non-enabled categories
            logging.debug('get request to: %s', url)
            async with session.get(str(url)) as resp:
                raw_html = await resp.text()
            # TODO: sum of requests and inc for one use db
            AdminHelper.increase_scheduled_requests()
        return raw_html
