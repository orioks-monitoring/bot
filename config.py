import os
import json


TELEGRAM_BOT_API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')

BASEDIR = os.path.dirname(os.path.abspath(__file__))
STUDENT_FILE_JSON_MASK = '{id}.json'

notify_settings_btns = (
    'notify_settings-marks',
    'notify_settings-news',
    'notify_settings-discipline_sources',
    'notify_settings-homeworks',
    'notify_settings-requests'
)

TELEGRAM_ADMIN_IDS_LIST = json.loads(os.environ['TELEGRAM_ADMIN_IDS_LIST'])

ORIOKS_MAX_LOGIN_TRIES = 10

TELEGRAM_STICKER_LOADER = 'CAACAgIAAxkBAAEEIlpiLSwO28zurkSJGRj6J9SLBIAHYQACIwADKA9qFCdRJeeMIKQGIwQ'

ORIOKS_PAGE_URLS = {
    'login': 'https://orioks.miet.ru/user/login',
    'notify': {
        'marks': 'https://orioks.miet.ru/student/student',
    }
}
