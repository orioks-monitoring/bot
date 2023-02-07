import asyncio
import logging
import os
import pickle
import random

import aiohttp
import aioschedule

from app.exceptions import OrioksParseDataException, CheckBaseException
from app.helpers import CommonHelper, TelegramMessageHelper, UserHelper
from app.helpers.ClientSessionHelper import ClientSessionHelper
from app.models.users import UserStatus, UserNotifySettings
from checking.marks.get_orioks_marks import user_marks_check
from checking.news.get_orioks_news import (
    user_news_check_from_news_id,
    get_current_new_info,
)
from checking.homeworks.get_orioks_homeworks import user_homeworks_check
from checking.requests.get_orioks_requests import user_requests_check
from http.cookies import SimpleCookie
from config import config


def _get_user_orioks_cookies_from_telegram_id(
    user_telegram_id: int,
) -> SimpleCookie:
    path_to_cookies = os.path.join(
        config.BASEDIR, 'users_data', 'cookies', f'{user_telegram_id}.pkl'
    )
    return SimpleCookie(pickle.load(open(path_to_cookies, 'rb')))


def _delete_users_tracking_data_in_notify_settings_off(
    user_telegram_id: int, user_notify_settings: UserNotifySettings
) -> None:
    if not user_notify_settings.marks:
        CommonHelper.safe_delete(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'marks',
                f'{user_telegram_id}.json',
            )
        )
    if not user_notify_settings.news:
        CommonHelper.safe_delete(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'news',
                f'{user_telegram_id}.json',
            )
        )
    if not user_notify_settings.discipline_sources:
        CommonHelper.safe_delete(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'discipline_sources',
                f'{user_telegram_id}.json',
            )
        )
    if not user_notify_settings.homeworks:
        CommonHelper.safe_delete(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'homeworks',
                f'{user_telegram_id}.json',
            )
        )
    if not user_notify_settings.requests:
        CommonHelper.safe_delete(
            os.path.join(
                config.PATH_TO_STUDENTS_TRACKING_DATA,
                'requests',
                f'{user_telegram_id}.json',
            )
        )


async def make_one_user_check(user_telegram_id: int) -> None:
    user_notify_settings = UserHelper.get_user_settings_by_telegram_id(
        user_telegram_id=user_telegram_id
    )
    cookies = _get_user_orioks_cookies_from_telegram_id(
        user_telegram_id=user_telegram_id
    )
    async with ClientSessionHelper(
        user_telegram_id=user_telegram_id,
        cookies=cookies,
        timeout=config.REQUESTS_TIMEOUT,
        headers=config.ORIOKS_REQUESTS_HEADERS,
    ) as session:
        try:
            if user_notify_settings.marks:
                await user_marks_check(
                    user_telegram_id=user_telegram_id, session=session
                )
            if user_notify_settings.discipline_sources:
                pass  # TODO: user_discipline_sources_check(user_telegram_id=user_telegram_id, session=session)
            if user_notify_settings.homeworks:
                await user_homeworks_check(
                    user_telegram_id=user_telegram_id, session=session
                )
            if user_notify_settings.requests:
                await user_requests_check(
                    user_telegram_id=user_telegram_id, session=session
                )
        except CheckBaseException:
            await UserHelper.increment_failed_request_count(user_telegram_id)
        else:
            UserHelper.reset_failed_request_count(user_telegram_id)

    _delete_users_tracking_data_in_notify_settings_off(
        user_telegram_id=user_telegram_id,
        user_notify_settings=user_notify_settings,
    )


async def make_all_users_news_check(tries_counter: int = 0) -> list:
    tasks = []
    users_to_check_news = UserHelper.get_users_with_enabled_news_subscription()
    users_to_check_news = [
        user.user_telegram_id for user in users_to_check_news
    ]
    if len(users_to_check_news) == 0:
        return []
    picked_user_to_check_news = random.choice(list(users_to_check_news))
    if tries_counter > 10:
        return []
    cookies = _get_user_orioks_cookies_from_telegram_id(
        user_telegram_id=picked_user_to_check_news
    )
    try:
        async with ClientSessionHelper(
            user_telegram_id=picked_user_to_check_news,
            cookies=cookies,
            timeout=config.REQUESTS_TIMEOUT,
            headers=config.ORIOKS_REQUESTS_HEADERS,
        ) as session:
            current_news = await get_current_new_info(
                user_telegram_id=picked_user_to_check_news, session=session
            )
    except OrioksParseDataException:
        await UserHelper.increment_failed_request_count(
            picked_user_to_check_news
        )
        return await make_all_users_news_check(tries_counter=tries_counter + 1)
    for user_telegram_id in users_to_check_news:
        try:
            cookies = _get_user_orioks_cookies_from_telegram_id(
                user_telegram_id=user_telegram_id
            )
        except FileNotFoundError:
            logging.error('(COOKIES) FileNotFoundError: %s', user_telegram_id)
            await UserHelper.increment_failed_request_count(user_telegram_id)
            continue
        user_session = ClientSessionHelper(
            user_telegram_id=user_telegram_id,
            cookies=cookies,
            timeout=config.REQUESTS_TIMEOUT,
        )
        tasks.append(
            user_news_check_from_news_id(
                user_telegram_id=user_telegram_id,
                session=user_session,
                current_news=current_news,
            )
        )
    return tasks


async def run_requests(tasks: list) -> None:
    try:
        await asyncio.gather(*tasks)
    except asyncio.TimeoutError:
        logging.error('Сервер ОРИОКС не отвечает')
    except aiohttp.ClientResponseError as exception:
        if exception.status == 504:
            logging.error(
                'Вероятно, на сервере ОРИОКС проводятся технические работы: %s',
                exception,
            )
        else:
            logging.error('Ошибка в запросах ОРИОКС!\n %s', exception)
            CommonHelper.print_traceback(exception)
            await TelegramMessageHelper.message_to_admins(
                message=f'Ошибка в запросах ОРИОКС!\n{exception}'
            )
    except Exception as exception:
        logging.error('Ошибка в запросах ОРИОКС!\n %s', exception)
        CommonHelper.print_traceback(exception)
        await TelegramMessageHelper.message_to_admins(
            message=f'Ошибка в запросах ОРИОКС!\n{exception}'
        )


async def do_checks():
    logging.info('checking started')

    authenticated_users = UserStatus.query.filter_by(authenticated=True)
    users_telegram_ids = set(
        user.user_telegram_id for user in authenticated_users
    )

    tasks = [] + await make_all_users_news_check()
    for user_telegram_id in users_telegram_ids:
        tasks.append(make_one_user_check(user_telegram_id=user_telegram_id))
    await run_requests(tasks=tasks)
    logging.info('checking ended')


async def scheduler():
    await TelegramMessageHelper.message_to_admins(message='Бот запущен!')
    aioschedule.every(config.ORIOKS_SECONDS_BETWEEN_WAVES).seconds.do(
        do_checks
    )
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
