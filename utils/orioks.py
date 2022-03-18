import os
import pickle

import aiohttp
from bs4 import BeautifulSoup

import config
import db
import utils.exeptions


async def orioks_login_save_cookies(user_login: int, user_password: str, user_telegram_id: int) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(config.ORIOKS_PAGE_URLS['login']) as resp:
            bs_content = BeautifulSoup(await resp.text(), "html.parser")
        _csrf_token = bs_content.find('input', {'name': '_csrf'})['value']
        login_data = {
            'LoginForm[login]': int(user_login),
            'LoginForm[password]': str(user_password),
            'LoginForm[rememberMe]': 1,
            '_csrf': _csrf_token,
        }
        async with session.post(config.ORIOKS_PAGE_URLS['login'], data=login_data) as resp:
            if str(resp.url) == config.ORIOKS_PAGE_URLS['login']:
                raise utils.exeptions.OrioksInvalidLoginCredsError
        cookies = session.cookie_jar.filter_cookies(resp.url)
    pickle.dump(cookies, open(os.path.join(config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl'), 'wb'))


def _safe_delete(path: str) -> None:
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def make_orioks_logout(user_telegram_id: int) -> None:
    _safe_delete(os.path.join(config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl'))
    path_to_tracking_data = os.path.join(config.BASEDIR, 'users_data', 'tracking_data')
    _safe_delete(os.path.join(path_to_tracking_data, 'discipline_sources', f'{user_telegram_id}.pkl'))
    _safe_delete(os.path.join(path_to_tracking_data, 'news', f'{user_telegram_id}.pkl'))
    _safe_delete(os.path.join(path_to_tracking_data, 'marks', f'{user_telegram_id}.pkl'))
    _safe_delete(os.path.join(path_to_tracking_data, 'homeworks', f'{user_telegram_id}.pkl'))
    _safe_delete(os.path.join(path_to_tracking_data, 'requests', f'{user_telegram_id}.pkl'))

    db.update_user_orioks_authenticated_status(user_telegram_id=user_telegram_id, is_user_orioks_authenticated=False)
