import sqlite3
import os

from config import Config


def get_user_notify_settings_to_dict(user_telegram_id: int) -> dict:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'select_all_from_user_notify_settings.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    raw = sql.execute(sql_script, {'user_telegram_id': user_telegram_id}).fetchone()
    db.close()
    return {
        'marks': True if raw[0] else False,
        'news': True if raw[1] else False,
        'discipline_sources': True if raw[2] else False,
        'homeworks': True if raw[3] else False,
        'requests': True if raw[4] else False,
    }


def update_user_notify_settings(user_telegram_id: int, row_name: str, to_value: bool) -> None:
    """
    row_name must only be in (marks, news, discipline_sources, homeworks, requests)
    """
    if row_name not in ('marks', 'news', 'discipline_sources', 'homeworks', 'requests'):
        raise Exception('update_user_notify_settings() -> row_name must only be in ('
                        'marks, news, discipline_sources, homeworks, requests)')
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'update_user_notify_settings_set_row_name.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script.format(row_name=row_name), {
        'to_value': to_value,
        'user_telegram_id': user_telegram_id
    })
    db.commit()
    db.close()


def update_user_notify_settings_reset_to_default(user_telegram_id: int) -> None:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'update_user_notify_settings_reset_to_default.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script, {
        'user_telegram_id': user_telegram_id,
        'marks': True,
        'news': False,
        'discipline_sources': False,
        'homeworks': False,
        'requests': False,
    })
    db.commit()
    db.close()


def select_all_news_enabled_users() -> set:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'select_all_news_enabled_users.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    result = set()
    for user in sql.execute(sql_script).fetchall():
        result.add(user[0])
    db.close()
    return result
