import os
import sqlite3
from typing import Set

"""User status"""

PATH_TO_SQL_FOLDER = 'sql'


def user_first_add_to_db(user_telegram_id: int) -> None:
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()

    with open(os.path.join(PATH_TO_SQL_FOLDER, 'create_user_status.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script)
    with open(os.path.join(PATH_TO_SQL_FOLDER, 'init_user_status.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script, {
        'user_telegram_id': user_telegram_id,
        'is_user_agreement_accepted': False,
        'is_user_orioks_authenticated': False,
        'orioks_login_attempts': 0
    })

    with open(os.path.join(PATH_TO_SQL_FOLDER, 'create_user_notify_settings.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script)

    with open(os.path.join(PATH_TO_SQL_FOLDER, 'init_user_notify_settings.sql'), 'r') as sql_file:
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


def get_user_agreement_status(user_telegram_id: int) -> bool:
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()

    with open(os.path.join(PATH_TO_SQL_FOLDER, 'select_is_user_agreement_accepted_from_user_status.sql'),
              'r') as sql_file:
        sql_script = sql_file.read()
    is_user_agreement_accepted = sql.execute(sql_script, {'user_telegram_id': user_telegram_id}).fetchone()[0]
    db.close()
    return is_user_agreement_accepted


def get_user_orioks_authenticated_status(user_telegram_id: int) -> bool:
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()
    with open(os.path.join(PATH_TO_SQL_FOLDER, 'select_is_user_orioks_authenticated_from_user_status.sql'),
              'r') as sql_file:
        sql_script = sql_file.read()
    is_user_orioks_authenticated = sql.execute(sql_script, {'user_telegram_id': user_telegram_id}).fetchone()[0]
    db.close()
    return is_user_orioks_authenticated


def update_user_agreement_status(user_telegram_id: int, is_user_agreement_accepted: bool) -> None:
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()
    with open(os.path.join(PATH_TO_SQL_FOLDER, 'update_user_status_set_is_user_agreement_accepted.sql'),
              'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script, {
        'is_user_agreement_accepted': is_user_agreement_accepted,
        'user_telegram_id': user_telegram_id
    })
    db.commit()
    db.close()


def update_user_orioks_authenticated_status(user_telegram_id: int, is_user_orioks_authenticated: bool) -> None:
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()
    with open(os.path.join(PATH_TO_SQL_FOLDER, 'update_user_status_set_is_user_orioks_authenticated.sql'),
              'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script, {
        'is_user_orioks_authenticated': is_user_orioks_authenticated,
        'user_telegram_id': user_telegram_id
    })
    db.commit()
    db.close()


def select_all_orioks_authenticated_users() -> Set[int]:
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()
    with open(os.path.join(PATH_TO_SQL_FOLDER, 'select_all_orioks_authenticated_users.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    result = set()
    for user in sql.execute(sql_script).fetchall():
        result.add(user[0])
    db.close()
    return result


def get_user_orioks_attempts(user_telegram_id: int) -> int:
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()
    with open(os.path.join(PATH_TO_SQL_FOLDER, 'select_user_orioks_attempts_from_user_status.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    attempts = sql.execute(sql_script, {'user_telegram_id': user_telegram_id}).fetchone()[0]
    db.close()
    return attempts


def update_inc_user_orioks_attempts(user_telegram_id: int) -> None:
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()
    with open(os.path.join(PATH_TO_SQL_FOLDER, 'update_inc_user_orioks_attempts.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script, {
        'to_value': int(get_user_orioks_attempts(user_telegram_id=user_telegram_id)) + 1,
        'user_telegram_id': user_telegram_id
    })
    db.commit()
    db.close()


"""Notify settings"""


def get_user_notify_settings_to_dict(user_telegram_id: int) -> dict:
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()
    with open(os.path.join(PATH_TO_SQL_FOLDER, 'select_all_from_user_notify_settings.sql'), 'r') as sql_file:
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
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()
    with open(os.path.join(PATH_TO_SQL_FOLDER, 'update_user_notify_settings_set_row_name.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script.format(row_name=row_name), {
        'to_value': to_value,
        'user_telegram_id': user_telegram_id
    })
    db.commit()
    db.close()


"""Admins statistics"""


def select_count_notify_settings_statistics() -> dict:
    """
    row_name must only be in (marks, news, discipline_sources, homeworks, requests)
    """
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()
    with open(os.path.join(PATH_TO_SQL_FOLDER, 'select_count_notify_settings_statistics.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    marks = sql.execute(sql_script.format(row_name='marks')).fetchone()
    news = sql.execute(sql_script.format(row_name='news')).fetchone()
    discipline_sources = sql.execute(sql_script.format(row_name='discipline_sources')).fetchone()
    homeworks = sql.execute(sql_script.format(row_name='homeworks')).fetchone()
    requests = sql.execute(sql_script.format(row_name='requests')).fetchone()
    db.close()
    return {
        'marks': marks[0],
        'news': news[0],
        'discipline_sources': discipline_sources[0],
        'homeworks': homeworks[0],
        'requests': requests[0],
    }


def select_count_user_status_statistics() -> dict:
    db = sqlite3.connect('orioks-monitoring_bot.db')
    sql = db.cursor()
    with open(os.path.join(PATH_TO_SQL_FOLDER, 'select_count_user_status_statistics.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    users_agreement_accepted = sql.execute(
        sql_script.format(row_name='is_user_agreement_accepted'), {
            'value': True,
        }
    ).fetchone()
    users_agreement_discarded = sql.execute(
        sql_script.format(row_name='is_user_agreement_accepted'), {
            'value': False,
        }
    ).fetchone()

    users_orioks_authentication = sql.execute(
        sql_script.format(row_name='is_user_orioks_authenticated'), {
            'value': True,
        }
    ).fetchone()
    users_orioks_no_authentication = sql.execute(
        sql_script.format(row_name='is_user_orioks_authenticated'), {
            'value': False,
        }
    ).fetchone()
    db.close()
    all_users = users_agreement_discarded[0] + users_agreement_accepted[0]
    all_orioks_users = users_orioks_no_authentication[0] + users_orioks_authentication[0]
    return {
        'Приняли пользовательское соглашение': f'{users_agreement_accepted[0]} / {all_users}',
        'Выполнили вход в ОРИОКС': f'{users_orioks_authentication[0]} / {all_orioks_users}',
    }
