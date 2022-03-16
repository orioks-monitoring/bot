import os
import pickle

import aiohttp
from bs4 import BeautifulSoup

import config
import utils.exeptions

ORIOKS_LOGIN_URL = 'https://orioks.miet.ru/user/login'


async def orioks_login_save_cookies(user_login: int, user_password: str, user_telegram_id: int) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(ORIOKS_LOGIN_URL) as resp:
            bs_content = BeautifulSoup(await resp.text(), "html.parser")
        _csrf_token = bs_content.find('input', {'name': '_csrf'})['value']
        login_data = {
            'LoginForm[login]': int(user_login),
            'LoginForm[password]': str(user_password),
            'LoginForm[rememberMe]': 1,
            '_csrf': _csrf_token,
        }
        async with session.post(ORIOKS_LOGIN_URL, data=login_data) as resp:
            if str(resp.url) == ORIOKS_LOGIN_URL:
                raise utils.exeptions.OrioksInvalidLoginCredsError
        cookies = session.cookie_jar.filter_cookies(resp.url)
    pickle.dump(cookies, open(os.path.join(config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl'), 'wb'))
