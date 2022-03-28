import os
import pickle

import re
import aiohttp
from bs4 import BeautifulSoup

import config
from utils.json_files import JsonFile
from utils.notify_to_user import notify_admins, notify_user
import aiogram.utils.markdown as md


def _orioks_parse_news(raw_html: str) -> dict:
    bs_content = BeautifulSoup(raw_html, "html.parser")
    news_raw = bs_content.find(id='news')
    last_news_line = news_raw.select_one('#news tr:nth-child(2) a')['href']
    last_news_id = int(re.findall(r'\d+$', last_news_line)[0])
    return {
        'last_id': last_news_id
    }


async def get_orioks_news(session: aiohttp.ClientSession) -> dict:
    async with session.get(config.ORIOKS_PAGE_URLS['notify']['news']) as resp:
        raw_html = await resp.text()
    return _orioks_parse_news(raw_html)


def _find_in_str_with_beginning_and_ending(string_to_find: str, beginning: str, ending: str) -> str:
    regex_result = re.findall(rf'{beginning}[\S\s]+{ending}', string_to_find)[0]
    return regex_result.replace(beginning, '').replace(ending, '').strip()


async def get_news_to_msg(news_id: int, session: aiohttp.ClientSession) -> str:
    async with session.get(config.ORIOKS_PAGE_URLS['masks']['news'].format(id=news_id)) as resp:
        raw_html = await resp.text()
    bs_content = BeautifulSoup(raw_html, "html.parser")
    well_raw = bs_content.find_all('div', {'class': 'well'})[0]

    news_name = _find_in_str_with_beginning_and_ending(
        string_to_find=well_raw.text,
        beginning='Заголовок:',
        ending='Тело новости:'
    )

    return md.text(
        md.text(
            md.text('📰'),
            md.hbold(news_name),
            sep=' '
        ),
        md.text(),
        md.text(
            md.text('Опубликована новость, подробности по ссылке:'),
            md.text(config.ORIOKS_PAGE_URLS['masks']['news'].format(id=news_id)),
            sep=' ',
        ),
        sep='\n',
    )  # TODO: сюда бы еще картиночку красивую типа такую, только с лого-глазом, газетой, заголовком новости, QR-кодом:
    #           https://techcrunch.com/wp-content/uploads/2022/01/silvergate-diem-meta-facebook.jpg


async def user_news_check(user_telegram_id: int, session: aiohttp.ClientSession):
    last_news_id = await get_orioks_news(session=session)
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
        try:
            msg_to_send = await get_news_to_msg(news_id=news_id, session=session)
            await notify_user(user_telegram_id=user_telegram_id, message=msg_to_send)
        except IndexError:
            pass  # id новостей могут идти не по порядку, поэтому надо игнорировать IndexError
    JsonFile.save(data=last_news_id, filename=path_users_to_file)
    return True
