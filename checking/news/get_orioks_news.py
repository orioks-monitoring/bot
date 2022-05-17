import logging
import os

import re
import aiohttp
from bs4 import BeautifulSoup

import config
from utils import exceptions
from utils.json_files import JsonFile
from utils.make_request import get_request
from utils.notify_to_user import SendToTelegram
import aiogram.utils.markdown as md
from images.imager import Imager
from utils.delete_file import safe_delete
from typing import NamedTuple


class NewsObject(NamedTuple):
    headline_news: str
    url: str
    id: int


def _orioks_parse_news(raw_html: str) -> dict:
    bs_content = BeautifulSoup(raw_html, "html.parser")
    news_raw = bs_content.find(id='news')
    if news_raw is None:
        raise exceptions.OrioksCantParseData
    last_news_line = news_raw.select_one('#news tr:nth-child(2) a')['href']
    last_news_id = int(re.findall(r'\d+$', last_news_line)[0])
    return {
        'last_id': last_news_id
    }


async def get_orioks_news(session: aiohttp.ClientSession) -> dict:
    raw_html = await get_request(url=config.ORIOKS_PAGE_URLS['notify']['news'], session=session)
    return _orioks_parse_news(raw_html)


def _find_in_str_with_beginning_and_ending(string_to_find: str, beginning: str, ending: str) -> str:
    regex_result = re.findall(rf'{beginning}[\S\s]+{ending}', string_to_find)[0]
    return regex_result.replace(beginning, '').replace(ending, '').strip()


async def get_news_by_news_id(news_id: int, session: aiohttp.ClientSession) -> NewsObject:
    raw_html = await get_request(url=config.ORIOKS_PAGE_URLS['masks']['news'].format(id=news_id), session=session)
    bs_content = BeautifulSoup(raw_html, "html.parser")
    well_raw = bs_content.find_all('div', {'class': 'well'})[0]
    return NewsObject(
        headline_news=_find_in_str_with_beginning_and_ending(
            string_to_find=well_raw.text,
            beginning='Заголовок:',
            ending='Тело новости:'),
        url=config.ORIOKS_PAGE_URLS['masks']['news'].format(id=news_id),
        id=news_id
    )


def transform_news_to_msg(news_obj: NewsObject) -> str:
    return md.text(
        md.text(
            md.text('📰'),
            md.hbold(news_obj.headline_news),
            sep=' '
        ),
        md.text(),
        md.text(
            md.text('Опубликована новость, подробности по ссылке:'),
            md.text(news_obj.url),
            sep=' ',
        ),
        sep='\n',
    )


async def get_current_new(user_telegram_id: int, session: aiohttp.ClientSession) -> NewsObject:
    student_json_file = config.STUDENT_FILE_JSON_MASK.format(id=user_telegram_id)
    path_users_to_file = os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'news', student_json_file)
    try:
        last_news_id = await get_orioks_news(session=session)
    except exceptions.OrioksCantParseData:
        logging.info('(NEWS) exception: utils.exceptions.OrioksCantParseData')
        safe_delete(path=path_users_to_file)
        raise exceptions.OrioksCantParseData
    return await get_news_by_news_id(news_id=last_news_id['last_id'], session=session)


async def user_news_check_from_news_id(user_telegram_id: int, session: aiohttp.ClientSession,
                                       current_new: NewsObject) -> None:
    student_json_file = config.STUDENT_FILE_JSON_MASK.format(id=user_telegram_id)
    path_users_to_file = os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'news', student_json_file)
    last_news_id = {'last_id': current_new.id}
    if student_json_file not in os.listdir(os.path.dirname(path_users_to_file)):
        await JsonFile.save(data=last_news_id, filename=path_users_to_file)
        await session.close()
        return None
    old_json = await JsonFile.open(filename=path_users_to_file)
    if last_news_id['last_id'] == old_json['last_id']:
        await session.close()
        return None
    if old_json['last_id'] > last_news_id['last_id']:
        await SendToTelegram.message_to_admins(
            message=f'[{user_telegram_id}] - old_json["last_id"] > last_news_id["last_id"]'
        )
        await session.close()
        raise Exception(f'[{user_telegram_id}] - old_json["last_id"] > last_news_id["last_id"]')
    difference = last_news_id['last_id'] - old_json['last_id']
    for news_id in range(old_json['last_id'] + 1, old_json['last_id'] + difference + 1):
        if news_id == current_new.id:
            news_obj = current_new
        else:
            try:
                news_obj = await get_news_by_news_id(news_id=news_id, session=session)
            except IndexError:
                continue  # id новостей могут идти не по порядку, поэтому надо игнорировать IndexError
        path_to_img = Imager().get_image_news(
            title_text=news_obj.headline_news,
            side_text='Опубликована новость',
            url=news_obj.url
        )
        await SendToTelegram.photo_message_to_user(
            user_telegram_id=user_telegram_id,
            photo_path=path_to_img,
            caption=transform_news_to_msg(news_obj=news_obj)
        )
        await JsonFile.save(data={"last_id": news_id}, filename=path_users_to_file)
        safe_delete(path=path_to_img)
    await session.close()
    await JsonFile.save(data=last_news_id, filename=path_users_to_file)
