import asyncio
import logging
import os
import pickle

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from datetime import datetime

from app.exceptions import OrioksInvalidLoginCredentialsException
from app.helpers import (
    CommonHelper,
    UserHelper,
)

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
                    ) as resp:
                        bs_content = BeautifulSoup(
                            await resp.text(), "html.parser"
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
                    ) as resp:
                        if str(resp.url) == config.ORIOKS_PAGE_URLS['login']:
                            raise OrioksInvalidLoginCredentialsException
                except asyncio.TimeoutError as exception:
                    raise exception

                cookies = session.cookie_jar.filter_cookies(resp.url)
            pickle.dump(
                cookies,
                open(
                    os.path.join(
                        config.BASEDIR,
                        'users_data',
                        'cookies',
                        f'{user_telegram_id}.pkl',
                    ),
                    'wb',
                ),
            )
            await asyncio.sleep(1)

    @staticmethod
    def make_orioks_logout(user_telegram_id: int) -> None:
        CommonHelper.safe_delete(
            os.path.join(
                config.BASEDIR,
                'users_data',
                'cookies',
                f'{user_telegram_id}.pkl',
            )
        )
        CommonHelper.safe_delete(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'news',
                f'{user_telegram_id}.json',
            )
        )
        CommonHelper.safe_delete(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'marks',
                f'{user_telegram_id}.json',
            )
        )
        CommonHelper.safe_delete(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'homeworks',
                f'{user_telegram_id}.json',
            )
        )
        CommonHelper.safe_delete(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'requests',
                'questionnaire',
                f'{user_telegram_id}.json',
            )
        )
        CommonHelper.safe_delete(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'requests',
                'doc',
                f'{user_telegram_id}.json',
            )
        )
        CommonHelper.safe_delete(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'requests',
                'reference',
                f'{user_telegram_id}.json',
            )
        )

        UserHelper.update_authorization_status(
            user_telegram_id=user_telegram_id, is_authenticated=False
        )
        UserHelper.reset_notification_settings(
            user_telegram_id=user_telegram_id
        )
