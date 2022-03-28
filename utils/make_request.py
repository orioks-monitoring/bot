import db.admins_statistics
import aiohttp


async def get_request(url: str, session: aiohttp.ClientSession) -> str:
    async with session.get(str(url)) as resp:
        raw_html = await resp.text()
    db.admins_statistics.update_inc_admins_statistics_row_name(  # TODO: sum of requests and inc for one use db
        row_name=db.admins_statistics.AdminsStatisticsRowNames.orioks_scheduled_requests
    )
    return raw_html
