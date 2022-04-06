import asyncio
import logging
import os
import pickle
from datetime import datetime

import aiohttp
import aioschedule

import config
import db.notify_settings
import db.user_status
from checking.marks.get_orioks_marks import user_marks_check
from checking.news.get_orioks_news import user_news_check
from checking.homeworks.get_orioks_homeworks import user_homeworks_check
from checking.requests.get_orioks_requests import user_requests_check
from utils.notify_to_user import notify_admins
from contextvars import ContextVar
import utils.delete_file


def _get_user_orioks_cookies_from_telegram_id(user_telegram_id: int) -> aiohttp.CookieJar:
    path_to_cookies = os.path.join(config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl')
    return pickle.load(open(path_to_cookies, 'rb'))


def _delete_users_tracking_data_in_notify_settings_off(user_telegram_id: int, user_notify_settings: dict) -> None:
    if not user_notify_settings['marks']:
        utils.delete_file.safe_delete(
            os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'marks', f'{user_telegram_id}.json')
        )
    if not user_notify_settings['news']:
        utils.delete_file.safe_delete(
            os.path.join(config.PATH_TO_STUDENTS_TRACKING_DATA, 'news', f'{user_telegram_id}.json')
        )
    if not user_notify_settings['discipline_sources']:
        utils.delete_file.safe_delete(os.path.join(
            config.PATH_TO_STUDENTS_TRACKING_DATA, 'discipline_sources', f'{user_telegram_id}.json')
        )
    if not user_notify_settings['homeworks']:
        utils.delete_file.safe_delete(os.path.join(
            config.PATH_TO_STUDENTS_TRACKING_DATA, 'homeworks', f'{user_telegram_id}.json')
        )
    if not user_notify_settings['requests']:
        utils.delete_file.safe_delete(os.path.join(
            config.PATH_TO_STUDENTS_TRACKING_DATA, 'requests', f'{user_telegram_id}.json')
        )


async def make_one_user_check(user_telegram_id: int, users_to_one_more_check: ContextVar):
    """
    return is user need to check one more time
    """
    user_to_add = users_to_one_more_check.get()
    user_notify_settings = db.notify_settings.get_user_notify_settings_to_dict(user_telegram_id=user_telegram_id)
    cookies = _get_user_orioks_cookies_from_telegram_id(user_telegram_id=user_telegram_id)
    async with aiohttp.ClientSession(cookies=cookies, timeout=config.REQUESTS_TIMEOUT) as session:
        if user_notify_settings['marks']:
            if not await user_marks_check(user_telegram_id=user_telegram_id, session=session):
                user_to_add.add(user_telegram_id)
        if user_notify_settings['news']:
            await user_news_check(user_telegram_id=user_telegram_id, session=session)
        if user_notify_settings['discipline_sources']:
            pass  # TODO: user_discipline_sources_check(user_telegram_id=user_telegram_id, session=session)
        if user_notify_settings['homeworks']:
            if not await user_homeworks_check(user_telegram_id=user_telegram_id, session=session):
                user_to_add.add(user_telegram_id)
        if user_notify_settings['requests']:
            if not await user_requests_check(user_telegram_id=user_telegram_id, session=session):
                user_to_add.add(user_telegram_id)
    users_to_one_more_check.set(user_to_add)
    _delete_users_tracking_data_in_notify_settings_off(
        user_telegram_id=user_telegram_id,
        user_notify_settings=user_notify_settings
    )


async def do_checks():
    logging.info(f'started: {datetime.now().strftime("%H:%M:%S %d.%m.%Y")}')
    users_to_check = db.user_status.select_all_orioks_authenticated_users()
    users_to_one_more_check = ContextVar('users_to_one_more_check', default=set())
    tasks = []
    for user_telegram_id in users_to_check:
        tasks.append(make_one_user_check(
            user_telegram_id=user_telegram_id,
            users_to_one_more_check=users_to_one_more_check
        ))
    try:
        await asyncio.gather(*tasks)
    except asyncio.TimeoutError:
        return await notify_admins(message='Сервер ОРИОКС не отвечает')
    except Exception as e:
        logging.error(f'Ошибка в запросах ОРИОКС!\n{e}')
        await notify_admins(message=f'Ошибка в запросах ОРИОКС!\n{e}')

    tasks = []
    for user_telegram_id in users_to_one_more_check.get():
        tasks.append(make_one_user_check(
            user_telegram_id=user_telegram_id,
            users_to_one_more_check=users_to_one_more_check  # don't care about it
        ))
    try:
        await asyncio.gather(*tasks)
    except asyncio.TimeoutError:
        return await notify_admins(message='Сервер ОРИОКС в данный момент недоступен!')
    except Exception as e:
        logging.error(f'Ошибка в запросах ОРИОКС!\n{e}')
        await notify_admins(message=f'Ошибка в запросах ОРИОКС!\n{e}')
    logging.info(f'ended: {datetime.now().strftime("%H:%M:%S %d.%m.%Y")}')


async def scheduler():
    await notify_admins(message='Бот запущен!')
    aioschedule.every(10).minutes.do(do_checks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
