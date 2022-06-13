import asyncio
import logging
import os
import pickle

import aiohttp
from bs4 import BeautifulSoup

from datetime import datetime

from app import CommonHelper
from app.exceptions import OrioksInvalidLoginCredentialsException
from app.helpers import TelegramMessageHelper
from config import Config
import aiogram.utils.markdown as md

import db.user_status
import db.notify_settings

_sem = asyncio.Semaphore(Config.ORIOKS_LOGIN_QUEUE_SEMAPHORE_VALUE)


class OrioksHelper:

    @staticmethod
    async def orioks_login_save_cookies(user_login: int, user_password: str, user_telegram_id: int) -> None:
        # pylint: disable=protected-access
        user_queue = len(_sem._waiters) + 2
        if user_queue - 2 > 0:
            logging.info(f'login: {user_queue=}')
            _cats_queue_emoji = f'{"🐈" * (user_queue - 1)}🐈‍⬛'
            await TelegramMessageHelper.text_message_to_user(
                user_telegram_id=user_telegram_id,
                message=md.text(
                    md.text(_cats_queue_emoji),
                    md.text(
                        md.text(f'Твой номер в очереди на авторизацию: {user_queue}.'),
                        md.text('Ты получишь уведомление, когда она будет выполнена.'),
                        sep=' ',
                    ),
                    md.text('Это предотвращает слишком большую нагрузку на ОРИОКС'),
                    sep='\n',
                )
            )
        async with _sem:  # orioks dont die please
            async with aiohttp.ClientSession(
                    timeout=Config.REQUESTS_TIMEOUT,
                    headers=Config.ORIOKS_REQUESTS_HEADERS
            ) as session:
                try:
                    logging.info(f'request to login: {datetime.now().strftime("%H:%M:%S %d.%m.%Y")}')
                    async with session.get(str(Config.ORIOKS_PAGE_URLS['login'])) as resp:
                        bs_content = BeautifulSoup(await resp.text(), "html.parser")
                    _csrf_token = bs_content.find('input', {'name': '_csrf'})['value']
                    login_data = {
                        'LoginForm[login]': int(user_login),
                        'LoginForm[password]': str(user_password),
                        'LoginForm[rememberMe]': 1,
                        '_csrf': _csrf_token,
                    }
                except asyncio.TimeoutError as e:
                    raise e
                try:
                    async with session.post(str(Config.ORIOKS_PAGE_URLS['login']), data=login_data) as resp:
                        if str(resp.url) == Config.ORIOKS_PAGE_URLS['login']:
                            raise OrioksInvalidLoginCredentialsException
                except asyncio.TimeoutError as e:
                    raise e

                cookies = session.cookie_jar.filter_cookies(resp.url)
            pickle.dump(cookies,
                        open(os.path.join(Config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl'), 'wb'))
            await asyncio.sleep(1)

    @staticmethod
    def make_orioks_logout(user_telegram_id: int) -> None:
        CommonHelper.safe_delete(os.path.join(Config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl'))
        CommonHelper.safe_delete(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'discipline_sources', f'{user_telegram_id}.json'))
        CommonHelper.safe_delete(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'news', f'{user_telegram_id}.json'))
        CommonHelper.safe_delete(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'marks', f'{user_telegram_id}.json'))
        CommonHelper.safe_delete(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'homeworks', f'{user_telegram_id}.json'))
        CommonHelper.safe_delete(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', 'questionnaire', f'{user_telegram_id}.json'))
        CommonHelper.safe_delete(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', 'doc', f'{user_telegram_id}.json'))
        CommonHelper.safe_delete(os.path.join(Config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', 'reference', f'{user_telegram_id}.json'))

        db.user_status.update_user_orioks_authenticated_status(user_telegram_id=user_telegram_id, is_user_orioks_authenticated=False)
        db.notify_settings.update_user_notify_settings_reset_to_default(user_telegram_id=user_telegram_id)
