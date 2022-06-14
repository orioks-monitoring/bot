import sqlite3
import os
from dataclasses import dataclass

from config import config


@dataclass
class AdminsStatisticsRowNames:
    orioks_scheduled_requests: str = 'orioks_scheduled_requests'
    orioks_success_logins: str = 'orioks_success_logins'
    orioks_failed_logins: str = 'orioks_failed_logins'


def select_all_from_admins_statistics() -> dict:
    db = sqlite3.connect(config.PATH_TO_DB)
    sql = db.cursor()

    with open(os.path.join(config.PATH_TO_SQL_FOLDER, 'select_all_from_admins_statistics.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    rows = sql.execute(sql_script).fetchone()
    db.close()
    return {
        'Запланированные успешные запросы на сервера ОРИОКС': rows[0],
        'Успешные попытки авторизации ОРИОКС': f'{rows[1]} / {rows[1] + rows[2]}',
    }


def update_inc_admins_statistics_row_name(row_name: str) -> None:
    """
    row_name must only be in (orioks_scheduled_requests, orioks_success_logins, orioks_failed_logins)
    """
    if row_name not in ('orioks_scheduled_requests', 'orioks_success_logins', 'orioks_failed_logins'):
        raise Exception('update_inc_admins_statistics_row_name() -> row_name must only be in ('
                        'orioks_scheduled_requests, orioks_success_logins, orioks_failed_logins)')
    db = sqlite3.connect(config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(config.PATH_TO_SQL_FOLDER, 'update_inc_admins_statistics_row_name.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script.format(row_name=row_name), {
        'row_name': row_name
    })
    db.commit()
    db.close()


def select_count_user_status_statistics() -> dict:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'select_count_user_status_statistics.sql'), 'r') as sql_file:
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


def select_count_notify_settings_row_name(row_name: str) -> int:
    """
    row_name must only be in (marks, news, discipline_sources, homeworks, requests)
    """
    if row_name not in ('marks', 'news', 'discipline_sources', 'homeworks', 'requests'):
        raise Exception('select_count_notify_settings_row_name() -> row_name must only be in ('
                        'marks, news, discipline_sources, homeworks, requests)')
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'select_count_notify_settings_row_name.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    count_notify_settings_marks = sql.execute(sql_script.format(row_name=row_name)).fetchone()
    return int(count_notify_settings_marks[0])
