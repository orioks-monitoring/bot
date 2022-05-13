import sqlite3
import config
import os


def get_user_notify_settings_to_dict(user_telegram_id: int) -> dict:
    db = sqlite3.connect(config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(config.PATH_TO_SQL_FOLDER, 'select_all_from_user_notify_settings.sql'), 'r') as sql_file:
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
    db = sqlite3.connect(config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(config.PATH_TO_SQL_FOLDER, 'update_user_notify_settings_set_row_name.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    sql.execute(sql_script.format(row_name=row_name), {
        'to_value': to_value,
        'user_telegram_id': user_telegram_id
    })
    db.commit()
    db.close()


def select_count_notify_settings_statistics() -> dict:  # TODO: to admins_statistics file
    """
    row_name must only be in (marks, news, discipline_sources, homeworks, requests)
    """
    db = sqlite3.connect(config.PATH_TO_DB)
    sql = db.cursor()
    with open(os.path.join(config.PATH_TO_SQL_FOLDER, 'select_count_notify_settings_statistics.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    marks = sql.execute(sql_script.format(row_name='marks')).fetchone()
    news = sql.execute(sql_script.format(row_name='news')).fetchone()
    discipline_sources = sql.execute(sql_script.format(row_name='discipline_sources')).fetchone()
    homeworks = sql.execute(sql_script.format(row_name='homeworks')).fetchone()
    requests = sql.execute(sql_script.format(row_name='requests')).fetchone()
    db.close()
    # TODO: SELECT COUNT(*) FROM user_notify_settings INNER JOIN user_status on user_notify_settings.user_telegram_id = user_status.user_telegram_id WHERE user_notify_settings.{category} = 1 AND user_status.is_user_orioks_authenticated = 1;
    return {
        'marks': marks[0],
        'news': news[0],
        'discipline_sources': discipline_sources[0],
        'homeworks': homeworks[0],
        'requests': requests[0],
    }
