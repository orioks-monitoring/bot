import sqlite3
import os

from config import config


def user_first_add_to_db(user_telegram_id: int) -> None:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()

    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'create_user_status.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script)
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'init_user_status.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script, {
        'user_telegram_id': user_telegram_id,
        'is_user_agreement_accepted': False,
        'is_user_orioks_authenticated': False,
        'orioks_login_attempts': 0
    })

    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'create_user_notify_settings.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script)

    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'init_user_notify_settings.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script, {
        'user_telegram_id': user_telegram_id,
        'marks': True,
        'news': False,
        'discipline_sources': False,
        'homeworks': False,
        'requests': False
    })
    db.commit()
    db.close()
