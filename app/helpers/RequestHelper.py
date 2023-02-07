import asyncio
import logging

from aiohttp import ClientResponse
from aiohttp.typedefs import StrOrURL

from app.exceptions import ClientResponseErrorParamsException
from app.helpers import AdminHelper, ClientSessionHelper
from config import config


class RequestHelper:
    @staticmethod
    async def my_raise_for_status(
        response: ClientResponse,
        user_telegram_id: int | None = None,
        raw_html: str | None = None,
    ) -> None:
        if response.status >= 400:
            raise ClientResponseErrorParamsException(
                response.request_info,
                response.history,
                user_telegram_id=user_telegram_id,
                raw_html=raw_html if response.status >= 500 else None,
                status=response.status,
                message=response.reason,
                headers=response.headers,
            )

    _sem = asyncio.Semaphore(config.ORIOKS_REQUESTS_SEMAPHORE_VALUE)

    @staticmethod
    async def get_request(url: StrOrURL, session: ClientSessionHelper) -> str:
        async with RequestHelper._sem:
            await asyncio.sleep(config.ORIOKS_SECONDS_BETWEEN_REQUESTS)
            # TODO: is db.user_status.get_user_orioks_authenticated_status(user_telegram_id=user_telegram_id)
            #       else safe delete all user's file
            #       Обработать случай, когда пользователь к моменту достижения своей очереди разлогинился
            # TODO: is db.notify_settings.get_user_notify_settings_to_dict(user_telegram_id=user_telegram_id)
            #       else safe delete non-enabled categories
            logging.info(
                'from %s - GET request to: %s', session.user_telegram_id, url
            )

            async with session.get(str(url)) as response:
                raw_html = await response.text()
                await RequestHelper.my_raise_for_status(
                    response, session.user_telegram_id, raw_html
                )
                # TODO: sum of requests and inc for one use db
                AdminHelper.increase_scheduled_requests()
            return raw_html
