import asyncio
import os
import pickle

import aiohttp
from bs4 import BeautifulSoup

import config
import db.user_status
import utils.exeptions
from utils.delete_file import safe_delete


async def orioks_login_save_cookies(user_login: int, user_password: str, user_telegram_id: int) -> None:
    async with aiohttp.ClientSession(timeout=config.REQUESTS_TIMEOUT) as session:
        try:
            async with session.get(config.ORIOKS_PAGE_URLS['login']) as resp:
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
            async with session.post(config.ORIOKS_PAGE_URLS['login'], data=login_data) as resp:
                if str(resp.url) == config.ORIOKS_PAGE_URLS['login']:
                    raise utils.exeptions.OrioksInvalidLoginCredsError
        except asyncio.TimeoutError as e:
            raise e

        cookies = session.cookie_jar.filter_cookies(resp.url)
    pickle.dump(cookies, open(os.path.join(config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl'), 'wb'))


def make_orioks_logout(user_telegram_id: int) -> None:
    safe_delete(os.path.join(config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl'))

    safe_delete(os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'discipline_sources', f'{user_telegram_id}.json'))

    safe_delete(os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'news', f'{user_telegram_id}.json'))

    safe_delete(os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'marks', f'{user_telegram_id}.json'))

    safe_delete(os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'homeworks', f'{user_telegram_id}.json'))

    safe_delete(os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', 'questionnaire',
                             f'{user_telegram_id}.json'))
    safe_delete(os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', 'doc', f'{user_telegram_id}.json'))
    safe_delete(os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', 'reference',
                             f'{user_telegram_id}.json'))

    db.user_status.update_user_orioks_authenticated_status(
        user_telegram_id=user_telegram_id,
        is_user_orioks_authenticated=False
    )
