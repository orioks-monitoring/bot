import os
import pickle

import re
import aiohttp
from bs4 import BeautifulSoup

import config
from utils.json_files import JsonFile
from utils.notify_to_user import notify_admins, notify_user


def _orioks_parse_news(raw_html: str) -> dict:
    bs_content = BeautifulSoup(raw_html, "html.parser")
    news_raw = bs_content.find(id='news')
    last_news_line = news_raw.select_one('#news tr:nth-child(2) a')['href']
    last_news_id = int(re.findall(r'\d+$', last_news_line)[0])
    return {
        'last_id': last_news_id
    }


async def get_orioks_news(user_telegram_id: int) -> dict:
    path_to_cookies = os.path.join(config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl')
    async with aiohttp.ClientSession() as session:
        cookies = pickle.load(open(path_to_cookies, 'rb'))
        async with session.get(config.ORIOKS_PAGE_URLS['notify']['news'], cookies=cookies) as resp:
            raw_html = await resp.text()
    return _orioks_parse_news(raw_html)


async def get_news_to_msg(news_id: int, user_telegram_id: int) -> str:
    path_to_cookies = os.path.join(config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl')
    async with aiohttp.ClientSession() as session:
        cookies = pickle.load(open(path_to_cookies, 'rb'))
        async with session.get(config.ORIOKS_PAGE_URLS['masks']['news'].format(id=news_id), cookies=cookies) as resp:
            raw_html = await resp.text()
    bs_content = BeautifulSoup(raw_html, "html.parser")
    well_raw = bs_content.find_all('div', {'class': 'well'})[0]
    # todo: beautify it
    return well_raw.text


async def user_news_check(user_telegram_id: int):
    last_news_id = await get_orioks_news(user_telegram_id=user_telegram_id)
    student_json_file = config.STUDENT_FILE_JSON_MASK.format(id=user_telegram_id)
    path_users_to_file = os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'news', student_json_file)
    if student_json_file not in os.listdir(os.path.dirname(path_users_to_file)):
        JsonFile.save(data=last_news_id, filename=path_users_to_file)
        return False
    old_json = JsonFile.open(filename=path_users_to_file)
    if last_news_id['last_id'] == old_json['last_id']:
        return True
    if old_json['last_id'] > last_news_id['last_id']:
        await notify_admins(message=f'[{user_telegram_id}] - old_json["last_id"] > last_news_id["last_id"]')
        raise Exception(f'[{user_telegram_id}] - old_json["last_id"] > last_news_id["last_id"]')
    difference = last_news_id['last_id'] - old_json['last_id']
    for news_id in range(old_json['last_id'] + 1, old_json['last_id'] + difference + 1):
        msg_to_send = await get_news_to_msg(news_id=news_id, user_telegram_id=user_telegram_id)
        await notify_user(user_telegram_id=user_telegram_id, message=msg_to_send)
    JsonFile.save(data=last_news_id, filename=path_users_to_file)
    return True
