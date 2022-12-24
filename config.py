import os
import json
import aiohttp
from dotenv import load_dotenv


class Config:

    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    STUDENT_FILE_JSON_MASK = '{id}.json'
    PATH_TO_STUDENTS_TRACKING_DATA = os.path.join(
        BASEDIR, 'users_data', 'tracking_data'
    )

    PATH_TO_DB = os.path.join(BASEDIR, 'orioks-monitoring_bot.db')
    PATH_TO_SQL_FOLDER = os.path.join(BASEDIR, 'db', 'sql')

    notify_settings_btns = (
        'notify_settings-marks',
        'notify_settings-news',
        'notify_settings-discipline_sources',
        'notify_settings-homeworks',
        'notify_settings-requests',
    )
    notify_settings_names_to_vars = {
        'marks': 'Оценки',
        'news': 'Новости',
        'discipline_sources': 'Ресурсы',
        'homeworks': 'Домашние задания',
        'requests': 'Заявки',
    }

    ORIOKS_MAX_LOGIN_TRIES = 10

    TELEGRAM_STICKER_LOADER = 'CAACAgIAAxkBAAEEIlpiLSwO28zurkSJGRj6J9SLBIAHYQACIwADKA9qFCdRJeeMIKQGIwQ'

    REQUESTS_TIMEOUT = aiohttp.ClientTimeout(total=30)

    ORIOKS_SECONDS_BETWEEN_REQUESTS = 1.5
    ORIOKS_SECONDS_BETWEEN_WAVES = 5
    ORIOKS_REQUESTS_SEMAPHORE_VALUE = 1
    ORIOKS_LOGIN_QUEUE_SEMAPHORE_VALUE = 1

    ORIOKS_REQUESTS_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'User-Agent': 'orioks_monitoring/1.0 (Linux; aiohttp)',
    }

    ORIOKS_PAGE_URLS = {
        'login': 'https://orioks.miet.ru/user/login',
        'masks': {
            'news': 'https://orioks.miet.ru/main/view-news?id={id}',
            'homeworks': 'https://orioks.miet.ru/student/homework/view?id_thread={id}',
            'requests': {
                'questionnaire': 'https://orioks.miet.ru/request/questionnaire/view?id_thread={id}',  # not sure
                'doc': 'https://orioks.miet.ru/request/doc/view?id_thread={id}',  # not sure
                'reference': 'https://orioks.miet.ru/request/reference/view?id_thread={id}',
            },
        },
        'notify': {
            'marks': 'https://orioks.miet.ru/studen1t/student',
            'news': 'https://orioks.miet.ru',
            'homeworks': 'https://orioks.miet.ru/student/homework/list',
            'requests': {
                'questionnaire': 'https://orioks.miet.ru/request/questionnaire/list?AnketaTreadForm[status]=1,2,4,6,3,5,7&AnketaTreadForm[accept]=-1',
                'doc': 'https://orioks.miet.ru/request/doc/list?DocThreadForm[status]=1,2,4,6,3,5,7&DocThreadForm[type]=0',
                'reference': 'https://orioks.miet.ru/request/reference/list?ReferenceThreadForm[status]=1,2,4,6,3,5,7',
            },
        },
    }

    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        self.TELEGRAM_BOT_API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')
        self.TELEGRAM_ADMIN_IDS_LIST = json.loads(
            os.environ['TELEGRAM_ADMIN_IDS_LIST']
        )
        self.DATABASE_URL = os.getenv('DATABASE_URL')


config = Config()
