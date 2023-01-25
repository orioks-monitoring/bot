import logging
import os

import re
import aiohttp
from aiohttp import ClientResponseError
from bs4 import BeautifulSoup

from app.exceptions import OrioksParseDataException, FileCompareException
from app.helpers import (
    CommonHelper,
    RequestHelper,
    JsonFileHelper,
    TelegramMessageHelper,
)
from config import config
import aiogram.utils.markdown as md


def _orioks_parse_requests(raw_html: str, section: str) -> dict:
    new_messages_td_list_index = 7
    if section == 'questionnaire':
        new_messages_td_list_index = 6
    bs_content = BeautifulSoup(raw_html, "html.parser")
    if bs_content.select_one('.table.table-condensed.table-thread') is None:
        raise OrioksParseDataException
    table_raw = bs_content.select(
        '.table.table-condensed.table-thread tr:not(:first-child)'
    )
    requests = dict()
    for tr in table_raw:
        _thread_id = int(
            re.findall(r'\d+$', tr.find_all('td')[2].select_one('a')['href'])[
                0
            ]
        )
        requests[_thread_id] = {
            'status': tr.find_all('td')[1].text,
            'new_messages': int(
                tr.find_all('td')[new_messages_td_list_index]
                .select_one('b')
                .text
            ),
            'about': {
                'name': tr.find_all('td')[3].text,
                'url': config.ORIOKS_PAGE_URLS['masks']['requests'][
                    section
                ].format(id=_thread_id),
            },
        }
    return requests


async def get_orioks_requests(
    section: str, session: aiohttp.ClientSession
) -> dict:
    raw_html = await RequestHelper.get_request(
        url=config.ORIOKS_PAGE_URLS['notify']['requests'][section],
        session=session,
    )
    return _orioks_parse_requests(raw_html=raw_html, section=section)


async def get_requests_to_msg(diffs: list) -> str:
    message = ''
    for diff in diffs:
        if diff['type'] == 'new_status':
            message += md.text(
                md.text(
                    md.text('📄'),
                    md.text('Новые изменения по заявке'),
                    md.hbold(f"«{diff['about']['name']}»"),
                    sep=' ',
                ),
                md.text(
                    md.text('Статус заявки изменён на:'),
                    md.hcode(diff['current_status']),
                    sep=' ',
                ),
                md.text(),
                md.text(
                    md.text('Подробности по ссылке:'),
                    md.text(diff['about']['url']),
                    sep=' ',
                ),
                sep='\n',
            )
        elif diff['type'] == 'new_message':
            message += md.text(
                md.text(
                    md.text('📄'),
                    md.text('Новые изменения по заявке'),
                    md.hbold(f"«{diff['about']['name']}»"),
                    sep=' ',
                ),
                md.text(
                    md.text('Получено личное сообщение.'),
                    md.text(
                        md.text('Количество новых сообщений:'),
                        md.hcode(diff['current_messages']),
                        sep=' ',
                    ),
                    sep=' ',
                ),
                md.text(),
                md.text(
                    md.text('Подробности по ссылке:'),
                    md.text(diff['about']['url']),
                    sep=' ',
                ),
                sep='\n',
            )
        message += '\n' * 3
    return message


def compare(old_dict: dict, new_dict: dict) -> list:
    diffs = []
    for thread_id_old in old_dict:
        try:
            _ = new_dict[thread_id_old]
        except KeyError as exception:
            raise FileCompareException from exception
        if (
            old_dict[thread_id_old]['status']
            != new_dict[thread_id_old]['status']
        ):
            diffs.append(
                {
                    'type': 'new_status',  # or `new_message`
                    'current_status': new_dict[thread_id_old]['status'],
                    'about': new_dict[thread_id_old]['about'],
                }
            )
        elif (
            new_dict[thread_id_old]['new_messages']
            > old_dict[thread_id_old]['new_messages']
        ):
            diffs.append(
                {
                    'type': 'new_message',  # or `new_status`
                    'current_messages': new_dict[thread_id_old][
                        'new_messages'
                    ],
                    'about': new_dict[thread_id_old]['about'],
                }
            )
    return diffs


async def _user_requests_check_with_subsection(
    user_telegram_id: int, section: str, session: aiohttp.ClientSession
) -> None:
    student_json_file = config.STUDENT_FILE_JSON_MASK.format(
        id=user_telegram_id
    )
    path_users_to_file = os.path.join(
        config.BASEDIR,
        'users_data',
        'tracking_data',
        'requests',
        section,
        student_json_file,
    )
    try:
        requests_dict = await get_orioks_requests(
            section=section, session=session
        )
    except OrioksParseDataException as exception:
        logging.info(
            '(REQUESTS) [%s] exception: utils.exceptions.OrioksCantParseData',
            user_telegram_id,
        )
        CommonHelper.safe_delete(path=path_users_to_file)
        raise exception
    except ClientResponseError as exception:
        if 400 <= exception.status < 500:
            logging.info(
                '(REQUESTS) [%s] exception: aiohttp.ClientResponseError status in [400, 500). Raising OrioksCantParseData',
                user_telegram_id,
            )
            raise OrioksParseDataException from exception
        raise exception

    if student_json_file not in os.listdir(
        os.path.dirname(path_users_to_file)
    ):
        await JsonFileHelper.save(
            data=requests_dict, filename=path_users_to_file
        )
        return None

    _old_json = await JsonFileHelper.open(filename=path_users_to_file)
    old_dict = JsonFileHelper.convert_dict_keys_to_int(_old_json)
    try:
        diffs = compare(old_dict=old_dict, new_dict=requests_dict)
    except FileCompareException as exception:
        await JsonFileHelper.save(
            data=requests_dict, filename=path_users_to_file
        )
        raise exception

    if len(diffs) > 0:
        msg_to_send = await get_requests_to_msg(diffs=diffs)
        await TelegramMessageHelper.text_message_to_user(
            user_telegram_id=user_telegram_id, message=msg_to_send
        )
    await JsonFileHelper.save(data=requests_dict, filename=path_users_to_file)


async def user_requests_check(
    user_telegram_id: int, session: aiohttp.ClientSession
) -> None:
    for section in ('questionnaire', 'doc', 'reference'):
        await _user_requests_check_with_subsection(
            user_telegram_id=user_telegram_id, section=section, session=session
        )
