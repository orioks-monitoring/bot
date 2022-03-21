import json
import os
import pickle
from dataclasses import dataclass

import aiohttp
from bs4 import BeautifulSoup

import config
from checking.marks.compares import file_compares, get_msg_from_diff
import utils
from utils.json_files import JsonFile
from utils.notify_to_user import notify_admins, notify_user


def my_isdigit(x) -> bool:
    try:
        float(x)
        return True
    except ValueError:
        return False


@dataclass
class DisciplineBall:
    current: float = 0
    might_be: float = 0


def _get_orioks_forang(raw_html: str):
    """return: [{'subject': s, 'tasks': [t], 'ball': {'current': c, 'might_be': m}, ...]"""
    bs_content = BeautifulSoup(raw_html, "html.parser")
    forang_raw = bs_content.find(id='forang').text
    forang = json.loads(forang_raw)
    json_to_save = []
    for discipline in forang['dises']:
        discipline_ball = DisciplineBall()
        one_discipline = []
        for mark in discipline['segments'][0]['allKms']:
            alias = mark['sh']

            current_grade = mark['grade']['b']
            max_grade = mark['max_ball']

            one_discipline.append({'alias': alias, 'current_grade': current_grade, 'max_grade': max_grade})
            discipline_ball.current += current_grade if my_isdigit(current_grade) else 0
            discipline_ball.might_be += max_grade if my_isdigit(max_grade) and current_grade != '-' else 0
        json_to_save.append({
            'subject': discipline['name'],
            'tasks': one_discipline,
            'ball': {
                'current': discipline_ball.current,
                'might_be': discipline_ball.might_be,
            }
        })
    return json_to_save


async def get_orioks_marks(user_telegram_id: int):
    path_to_cookies = os.path.join(config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl')
    async with aiohttp.ClientSession() as session:
        cookies = pickle.load(open(path_to_cookies, 'rb'))
        async with session.get(config.ORIOKS_PAGE_URLS['notify']['marks'], cookies=cookies) as resp:
            raw_html = await resp.text()
    return _get_orioks_forang(raw_html)


async def user_marks_check(user_telegram_id: int) -> bool:
    """
    return is success, if not then check one more time
    """
    try:
        detailed_info = await get_orioks_marks(user_telegram_id=user_telegram_id)
    except FileNotFoundError:
        await notify_admins(message=f'FileNotFoundError - {user_telegram_id}')
        raise Exception(f'FileNotFoundError - {user_telegram_id}')
    student_json_file = config.STUDENT_FILE_JSON_MASK.format(id=user_telegram_id)
    path_users_to_file = os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'marks', student_json_file)

    if student_json_file not in os.listdir(os.path.dirname(path_users_to_file)):
        JsonFile.save(data=detailed_info, filename=path_users_to_file)
        return False
    old_json = JsonFile.open(filename=path_users_to_file)
    try:
        diffs = file_compares(old_file=old_json, new_file=detailed_info)
    except utils.exeptions.FileCompareError:
        JsonFile.save(data=detailed_info, filename=path_users_to_file)
        if old_json[0]['subject'] != detailed_info[0]['subject'] and \
                old_json[-1]['subject'] != detailed_info[-1]['subject']:
            await notify_admins(message=f'Похоже, что начался новый семестр!')
            await notify_user(
                user_telegram_id=user_telegram_id,
                message='Поздравляем с началом нового семестра и желаем успехов в учёбе!'
            )
        return False

    if len(diffs) > 0:
        msg = get_msg_from_diff(diffs)
        await notify_user(
            user_telegram_id=user_telegram_id,
            message=msg
        )
        JsonFile.save(data=detailed_info, filename=path_users_to_file)
    return True
