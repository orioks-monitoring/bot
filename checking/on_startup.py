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
import utils
from utils.notify_to_user import SendToTelegram
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


async def make_one_user_check(user_telegram_id: int) -> None:
    user_notify_settings = db.notify_settings.get_user_notify_settings_to_dict(user_telegram_id=user_telegram_id)
    cookies = _get_user_orioks_cookies_from_telegram_id(user_telegram_id=user_telegram_id)
    async with aiohttp.ClientSession(cookies=cookies, timeout=config.REQUESTS_TIMEOUT) as session:
        if user_notify_settings['marks']:
            await user_marks_check(user_telegram_id=user_telegram_id, session=session)
        if user_notify_settings['news']:
            await user_news_check(user_telegram_id=user_telegram_id, session=session)
        if user_notify_settings['discipline_sources']:
            pass  # TODO: user_discipline_sources_check(user_telegram_id=user_telegram_id, session=session)
        if user_notify_settings['homeworks']:
            await user_homeworks_check(user_telegram_id=user_telegram_id, session=session)
        if user_notify_settings['requests']:
            await user_requests_check(user_telegram_id=user_telegram_id, session=session)
    _delete_users_tracking_data_in_notify_settings_off(
        user_telegram_id=user_telegram_id,
        user_notify_settings=user_notify_settings
    )


async def run_requests(tasks: list) -> None:
    try:
        await asyncio.gather(*tasks)
    except asyncio.TimeoutError:
        return await SendToTelegram.message_to_admins(message='Сервер ОРИОКС не отвечает')
    except Exception as e:
        logging.error(f'Ошибка в запросах ОРИОКС!\n{e}')
        await SendToTelegram.message_to_admins(message=f'Ошибка в запросах ОРИОКС!\n{e}')


async def do_checks():
    logging.info(f'started: {datetime.now().strftime("%H:%M:%S %d.%m.%Y")}')
    users_to_check = db.user_status.select_all_orioks_authenticated_users()
    tasks = []
    for user_telegram_id in users_to_check:
        tasks.append(make_one_user_check(
            user_telegram_id=user_telegram_id
        ))
    await run_requests(tasks=tasks)
    logging.info(f'ended: {datetime.now().strftime("%H:%M:%S %d.%m.%Y")}')


async def scheduler():
    await SendToTelegram.message_to_admins(message='Бот запущен!')
    aioschedule.every(10).minutes.do(do_checks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
