import json
import os
import pickle
from dataclasses import dataclass

import aiohttp
from bs4 import BeautifulSoup

import config

ORIOKS_DISCIPLINE_BALLS = 'https://orioks.miet.ru/student/student'


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


async def _get_orioks_forang(raw_html: str):
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
        async with session.get(ORIOKS_DISCIPLINE_BALLS, cookies=cookies) as resp:
            raw_html = await resp.text()
    return await _get_orioks_forang(raw_html)
