import logging
import os

import re
from aiohttp import ClientResponseError
from bs4 import BeautifulSoup

from app.exceptions import OrioksParseDataException
from app.helpers import (
    RequestHelper,
    CommonHelper,
    JsonFileHelper,
    TelegramMessageHelper,
    MarksPictureHelper,
    ClientSessionHelper,
)
from config import config
import aiogram.utils.markdown as md
from typing import NamedTuple


class NewsObject(NamedTuple):
    headline_news: str
    url: str
    id: int


class ActualNews(NamedTuple):
    latest_id: int
    student_actual_news: set[int]
    last_new: NewsObject


def _get_student_actual_news(raw_html: str) -> set[int]:
    def __get_int_from_line(news_line: str) -> int:
        return int(re.findall(r'\d+$', news_line)[0])

    bs_content = BeautifulSoup(raw_html, "html.parser")
    news_raw = bs_content.find(id='news')
    if news_raw is None:
        raise OrioksParseDataException
    news_id = set(
        __get_int_from_line(x['href'])
        for x in news_raw.select('#news tr:not(:first-child) a')
    )
    return news_id


async def get_news_object_by_news_id(
    news_id: int, session: ClientSessionHelper
) -> NewsObject:
    raw_html = await RequestHelper.get_request(
        url=config.ORIOKS_PAGE_URLS['masks']['news'].format(id=news_id),
        session=session,
    )
    bs_content = BeautifulSoup(raw_html, "html.parser")
    well_raw = bs_content.find_all('div', {'class': 'well'})[0]
    return NewsObject(
        headline_news=_find_in_str_with_beginning_and_ending(
            string_to_find=well_raw.text,
            beginning='Заголовок:',
            ending='Тело новости:',
        ),
        url=config.ORIOKS_PAGE_URLS['masks']['news'].format(id=news_id),
        id=news_id,
    )


async def get_orioks_news(session: ClientSessionHelper) -> ActualNews:
    raw_html = await RequestHelper.get_request(
        url=config.ORIOKS_PAGE_URLS['notify']['news'], session=session
    )
    student_actual_news = _get_student_actual_news(raw_html)
    latest_id = max(student_actual_news)
    return ActualNews(
        latest_id=latest_id,
        student_actual_news=student_actual_news,
        last_new=await get_news_object_by_news_id(
            news_id=latest_id, session=session
        ),
    )


def _find_in_str_with_beginning_and_ending(
    string_to_find: str, beginning: str, ending: str
) -> str:
    regex_result = re.findall(rf'{beginning}[\S\s]+{ending}', string_to_find)[
        0
    ]
    return str(regex_result.replace(beginning, '').replace(ending, '').strip())


def transform_news_to_msg(news_obj: NewsObject) -> str:
    return str(
        md.text(
            md.text(md.text('📰'), md.hbold(news_obj.headline_news), sep=' '),
            md.text(),
            md.text(
                md.text('Опубликована новость, подробности по ссылке:'),
                md.text(news_obj.url),
                sep=' ',
            ),
            sep='\n',
        )
    )


async def get_current_new_info(
    user_telegram_id: int, session: ClientSessionHelper
) -> ActualNews:
    student_json_file = config.STUDENT_FILE_JSON_MASK.format(
        id=user_telegram_id
    )
    path_users_to_file = os.path.join(
        config.BASEDIR,
        'users_data',
        'tracking_data',
        'news',
        student_json_file,
    )
    try:
        last_news_ids: ActualNews = await get_orioks_news(session=session)
    except OrioksParseDataException as exception:
        logging.info(
            '(NEWS) [%s] exception: utils.exceptions.OrioksCantParseData',
            user_telegram_id,
        )
        CommonHelper.safe_delete(path=path_users_to_file)
        raise exception
    except ClientResponseError as exception:
        if 400 <= exception.status < 500:
            logging.info(
                '(NEWS) [%s] exception: aiohttp.ClientResponseError status in [400, 500). Raising OrioksCantParseData',
                user_telegram_id,
            )
            raise OrioksParseDataException from exception
        raise exception

    return last_news_ids


async def user_news_check_from_news_id(
    user_telegram_id: int,
    session: ClientSessionHelper,
    current_news: ActualNews,
) -> None:
    student_json_file = config.STUDENT_FILE_JSON_MASK.format(
        id=user_telegram_id
    )
    path_users_to_file = os.path.join(
        config.BASEDIR,
        'users_data',
        'tracking_data',
        'news',
        student_json_file,
    )
    if student_json_file not in os.listdir(
        os.path.dirname(path_users_to_file)
    ):
        await JsonFileHelper.save(
            data={'last_id': current_news.latest_id},
            filename=path_users_to_file,
        )
        await session.close()
        return None
    old_json = await JsonFileHelper.open(filename=path_users_to_file)
    if current_news.latest_id == old_json['last_id']:
        await session.close()
        return None
    if old_json['last_id'] > current_news.latest_id:
        await TelegramMessageHelper.message_to_admins(
            message=f'[{user_telegram_id}] - old_json["last_id"] > last_news_id["last_id"]'
        )
        await session.close()
        CommonHelper.safe_delete(path=path_users_to_file)
        raise Exception(
            f'[{user_telegram_id}] - old_json["last_id"] > last_news_id["last_id"]'
        )
    difference = current_news.latest_id - old_json['last_id']
    for news_id in range(
        old_json['last_id'] + 1, old_json['last_id'] + difference + 1
    ):
        if news_id not in current_news.student_actual_news:
            logging.info(
                'Новость с id %s существует, но не показывается в таблице на главной странице',
                news_id,
            )
            continue
        if news_id == current_news.latest_id:
            news_obj = current_news.last_new
        else:
            try:
                news_obj = await get_news_object_by_news_id(
                    news_id=news_id, session=session
                )
            except IndexError:
                continue  # id новостей могут идти не по порядку, поэтому надо игнорировать IndexError
        path_to_img = MarksPictureHelper().get_image_news(
            title_text=news_obj.headline_news,
            side_text='Опубликована новость',
            url=news_obj.url,
        )
        await TelegramMessageHelper.photo_message_to_user(
            user_telegram_id=user_telegram_id,
            photo_path=path_to_img,
            caption=transform_news_to_msg(news_obj=news_obj),
        )
        await JsonFileHelper.save(
            data={"last_id": news_id}, filename=path_users_to_file
        )
        CommonHelper.safe_delete(path=path_to_img)
    await session.close()
    await JsonFileHelper.save(
        data={'last_id': current_news.latest_id}, filename=path_users_to_file
    )
