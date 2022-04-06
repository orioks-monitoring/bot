import asyncio
import logging

import db.admins_statistics
import aiohttp


_sem = asyncio.Semaphore(1)


async def get_request(url: str, session: aiohttp.ClientSession) -> str:
    async with _sem:  # next coroutine(s) will stuck here until the previous is done
        await asyncio.sleep(2)  # orioks dont die please
        logging.debug(f'get request to: {url}')
        async with session.get(str(url)) as resp:
            raw_html = await resp.text()
        db.admins_statistics.update_inc_admins_statistics_row_name(  # TODO: sum of requests and inc for one use db
            row_name=db.admins_statistics.AdminsStatisticsRowNames.orioks_scheduled_requests
        )
    return raw_html
