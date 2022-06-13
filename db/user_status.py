import sqlite3
from typing import Set
import os

from config import Config


def get_user_agreement_status(user_telegram_id: int) -> bool:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()

    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'select_is_user_agreement_accepted_from_user_status.sql'),
              'r') as sql_file:
        sql_script = sql_file.read()
    is_user_agreement_accepted = bool(sql.execute(sql_script, {'user_telegram_id': user_telegram_id}).fetchone()[0])
    db.close()
    return is_user_agreement_accepted


def get_user_orioks_authenticated_status(user_telegram_id: int) -> bool:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'select_is_user_orioks_authenticated_from_user_status.sql'),
              'r') as sql_file:
        sql_script = sql_file.read()
    is_user_orioks_authenticated = bool(sql.execute(sql_script, {'user_telegram_id': user_telegram_id}).fetchone()[0])
    db.close()
    return is_user_orioks_authenticated


def update_user_agreement_status(user_telegram_id: int, is_user_agreement_accepted: bool) -> None:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'update_user_status_set_is_user_agreement_accepted.sql'),
              'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script, {
        'is_user_agreement_accepted': is_user_agreement_accepted,
        'user_telegram_id': user_telegram_id
    })
    db.commit()
    db.close()


def update_user_orioks_authenticated_status(user_telegram_id: int, is_user_orioks_authenticated: bool) -> None:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'update_user_status_set_is_user_orioks_authenticated.sql'),
              'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script, {
        'is_user_orioks_authenticated': is_user_orioks_authenticated,
        'user_telegram_id': user_telegram_id
    })
    db.commit()
    db.close()


def select_all_orioks_authenticated_users() -> Set[int]:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'select_all_orioks_authenticated_users.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    result = set()
    for user in sql.execute(sql_script).fetchall():
        result.add(user[0])
    db.close()
    return result


def get_user_orioks_attempts(user_telegram_id: int) -> int:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'select_user_orioks_attempts_from_user_status.sql'),
              'r') as sql_file:
        sql_script = sql_file.read()
    attempts = int(sql.execute(sql_script, {'user_telegram_id': user_telegram_id}).fetchone()[0])
    db.close()
    return attempts


def update_inc_user_orioks_attempts(user_telegram_id: int) -> None:
    db = sqlite3.connect(Config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(Config.PATH_TO_SQL_FOLDER, 'update_inc_user_orioks_attempts.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script, {
        'to_value': int(get_user_orioks_attempts(user_telegram_id=user_telegram_id)) + 1,
        'user_telegram_id': user_telegram_id
    })
    db.commit()
    db.close()
