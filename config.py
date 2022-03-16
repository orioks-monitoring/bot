import os

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
