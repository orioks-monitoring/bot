import asyncio
import logging

import config
import db.admins_statistics
import aiohttp


_sem = asyncio.Semaphore(config.ORIOKS_REQUESTS_SEMAPHORE_VALUE)


async def get_request(url: str, session: aiohttp.ClientSession) -> str:
    async with _sem:  # next coroutine(s) will stuck here until the previous is done
        await asyncio.sleep(config.ORIOKS_SECONDS_BETWEEN_REQUESTS)  # orioks dont die please
        # TODO: is db.user_status.get_user_orioks_authenticated_status(user_telegram_id=user_telegram_id)
        #       else safe delete all user's file
        # TODO: is db.notify_settings.get_user_notify_settings_to_dict(user_telegram_id=user_telegram_id)
        #       else safe delete non-enabled categories
        logging.debug(f'get request to: {url}')
        async with session.get(str(url)) as resp:
            raw_html = await resp.text()
        db.admins_statistics.update_inc_admins_statistics_row_name(  # TODO: sum of requests and inc for one use db
            row_name=db.admins_statistics.AdminsStatisticsRowNames.orioks_scheduled_requests
        )
    return raw_html
