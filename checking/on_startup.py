import asyncio
import os

import aioschedule

import config
import db
import utils.exeptions
from checking.compares import file_compares, get_msg_from_diff
from checking.get_orioks_marks import get_orioks_marks
from checking.json_files import JsonFile


async def user_marks_check(user_telegram_id: int) -> bool:
    """
    return is success, if not then check one more time
    """
    try:
        detailed_info = await get_orioks_marks(user_telegram_id=user_telegram_id)
    except FileNotFoundError:
        raise Exception(f'FileNotFoundError -> {user_telegram_id}')  # todo: notify to admins
    student_json_file = config.STUDENT_FILE_JSON_MASK.format(id=user_telegram_id)
    path_users_to_file = os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'marks', student_json_file)

    if student_json_file not in os.listdir(os.path.dirname(path_users_to_file)):
        print(f'[{user_telegram_id}] Скрипт запущен впервые?')  # todo: notify to admins or to Logger
        JsonFile.save(data=detailed_info, filename=path_users_to_file)
        return False
    old_json = JsonFile.open(filename=path_users_to_file)
    try:
        diffs = file_compares(old_file=old_json, new_file=detailed_info)
    except utils.exeptions.FileCompareError:
        JsonFile.save(data=detailed_info, filename=path_users_to_file)
        if old_json[0]['subject'] != detailed_info[0]['subject']:
            print(f'[{user_telegram_id}] Начался новый семестр! [notify!]')
        else:
            print(f'[{user_telegram_id}] Структура файла данных поменялась. [silent]')
        return False

    if len(diffs) > 0:
        msg = get_msg_from_diff(diffs)
        print(f'[{user_telegram_id}] {msg}')
        JsonFile.save(data=detailed_info, filename=path_users_to_file)
    else:
        print(f'[{user_telegram_id}] Изменений нет.')
    return True


async def do_checks():
    users_to_check = db.select_all_orioks_authenticated_users()
    users_to_one_more_check = set()
    for user_telegram_id in users_to_check:
        user_notify_settings = db.get_user_notify_settings_to_dict(user_telegram_id=user_telegram_id)
        if user_notify_settings['marks']:
            if not await user_marks_check(user_telegram_id=user_telegram_id):
                users_to_one_more_check.add(user_telegram_id)
        if user_notify_settings['news']:
            pass  # user_news_check(user_telegram_id=user_telegram_id)
        if user_notify_settings['discipline_sources']:
            pass  # user_discipline_sources_check(user_telegram_id=user_telegram_id)
        if user_notify_settings['homeworks']:
            pass  # user_homeworks_check(user_telegram_id=user_telegram_id)
        if user_notify_settings['requests']:
            pass  # user_requests_check(user_telegram_id=user_telegram_id)
    for user_telegram_id in users_to_one_more_check:
        await user_marks_check(user_telegram_id=user_telegram_id)


async def scheduler():
    aioschedule.every(5).minutes.do(do_checks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
