import asyncio
import logging
import os
import pickle

import aiohttp
import aioschedule

import config
import db.notify_settings
import db.user_status
import utils.notify_to_user
from checking.marks.get_orioks_marks import user_marks_check
from checking.news.get_orioks_news import user_news_check
from checking.homeworks.get_orioks_homeworks import user_homeworks_check
from checking.requests.get_orioks_requests import user_requests_check
from utils.notify_to_user import notify_admins
from contextvars import ContextVar


def _get_user_orioks_cookies_from_telegram_id(user_telegram_id: int) -> aiohttp.CookieJar:
    path_to_cookies = os.path.join(config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl')
    return pickle.load(open(path_to_cookies, 'rb'))


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


async def do_checks():
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


async def scheduler():
    await notify_admins(message='Бот запущен!')
    aioschedule.every(15).minutes.do(do_checks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
