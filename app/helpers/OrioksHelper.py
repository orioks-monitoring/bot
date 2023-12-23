import asyncio
import logging

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from datetime import datetime

from app.exceptions import OrioksInvalidLoginCredentialsException
from app.helpers.LoginLogoutHelper import LoginLogoutHelper
from app.helpers.CookiesHelper import CookiesHelper

from config import config

_sem = asyncio.Semaphore(config.ORIOKS_LOGIN_QUEUE_SEMAPHORE_VALUE)


class OrioksHelper:
    @staticmethod
    async def orioks_login_save_cookies(
        user_login: int, user_password: str, user_telegram_id: int
    ) -> None:
        # pylint: disable=protected-access
        async with _sem:
            async with ClientSession(
                timeout=config.REQUESTS_TIMEOUT,
                headers=config.ORIOKS_REQUESTS_HEADERS,
            ) as session:
                try:
                    logging.info(
                        'request to login: %s',
                        datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
                    )
                    async with session.get(
                        str(config.ORIOKS_PAGE_URLS['login'])
                    ) as response:
                        bs_content = BeautifulSoup(
                            await response.text(), "html.parser"
                        )
                    _csrf_token = bs_content.find('input', {'name': '_csrf'})[
                        'value'
                    ]
                    login_data = {
                        'LoginForm[login]': int(user_login),
                        'LoginForm[password]': str(user_password),
                        'LoginForm[rememberMe]': 1,
                        '_csrf': _csrf_token,
                    }
                except asyncio.TimeoutError as exception:
                    raise exception
                try:
                    async with session.post(
                        str(config.ORIOKS_PAGE_URLS['login']), data=login_data
                    ) as response:
                        if (
                            str(response.url)
                            == config.ORIOKS_PAGE_URLS['login']
                        ):
                            raise OrioksInvalidLoginCredentialsException
                except asyncio.TimeoutError as exception:
                    raise exception
                logging.info("Got cookies from orioks")

                cookies = CookiesHelper.encrypt_cookies_from_session(
                    session, response.url
                )

            await LoginLogoutHelper.make_login(cookies, user_telegram_id)
