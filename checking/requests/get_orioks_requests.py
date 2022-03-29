import os

import re
import aiohttp
from bs4 import BeautifulSoup

import config
from utils import exeptions
from utils.json_files import JsonFile
from utils.notify_to_user import notify_user
from utils.make_request import get_request
import aiogram.utils.markdown as md


def _orioks_parse_requests(raw_html: str, section: str) -> list:
    bs_content = BeautifulSoup(raw_html, "html.parser")
    table_raw = bs_content.select('.table.table-condensed.table-thread tr:not(:first-child)')
    requests = []
    for tr in table_raw:
        _thread_id = int(re.findall(r'\d+$', tr.find_all('td')[2].select_one('a')['href'])[0])
        requests.append({
            'thread_id': _thread_id,
            'status': tr.find_all('td')[1].text,
            'new_messages': int(tr.find_all('td')[7].select_one('b').text),
            'about': {
                'name': tr.find_all('td')[3].text,
                'url': config.ORIOKS_PAGE_URLS['masks']['requests'][section].format(id=_thread_id),
            },
        })
    return requests


async def get_orioks_requests(section: str, session: aiohttp.ClientSession) -> list:
    raw_html = await get_request(url=config.ORIOKS_PAGE_URLS['notify']['requests'][section], session=session)
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
                    sep=' '
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
                    sep=' '
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


def compare(old_list: list, new_list: list) -> list:
    diffs = []
    for old, new in zip(old_list, new_list):
        if old['thread_id'] != new['thread_id']:
            raise exeptions.FileCompareError
        if old['status'] != new['status']:
            diffs.append({
                'type': 'new_status',  # or `new_message`
                'current_status': new['status'],
                'about': new['about'],
            })
        elif new['new_messages'] > old['new_messages']:
            diffs.append({
                'type': 'new_message',  # or `new_status`
                'current_messages': new['new_messages'],
                'about': new['about'],
            })
    return diffs


async def _user_requests_check_with_subsection(user_telegram_id: int, section: str, session: aiohttp.ClientSession):
    requests_list = await get_orioks_requests(section=section, session=session)
    student_json_file = config.STUDENT_FILE_JSON_MASK.format(id=user_telegram_id)
    path_users_to_file = os.path.join(config.BASEDIR, 'users_data', 'tracking_data',
                                      'requests', section, student_json_file)
    if student_json_file not in os.listdir(os.path.dirname(path_users_to_file)):
        await JsonFile.save(data=requests_list, filename=path_users_to_file)
        return False

    old_json = await JsonFile.open(filename=path_users_to_file)
    if len(requests_list) != len(old_json):
        await JsonFile.save(data=requests_list, filename=path_users_to_file)
        return False
    try:
        diffs = compare(old_list=old_json, new_list=requests_list)
    except exeptions.FileCompareError:
        await JsonFile.save(data=requests_list, filename=path_users_to_file)
        return False

    if len(diffs) > 0:
        msg_to_send = await get_requests_to_msg(diffs=diffs)
        await notify_user(user_telegram_id=user_telegram_id, message=msg_to_send)
    await JsonFile.save(data=requests_list, filename=path_users_to_file)
    return True


async def user_requests_check(user_telegram_id: int, session: aiohttp.ClientSession) -> bool:
    is_need_one_more_check = False
    for section in ('questionnaire', 'doc', 'reference'):
        is_need_one_more_check |= await _user_requests_check_with_subsection(
            user_telegram_id=user_telegram_id,
            section=section,
            session=session
        )
    return is_need_one_more_check
