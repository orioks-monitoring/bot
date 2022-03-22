import asyncio

import aioschedule
import db
from checking.marks.get_orioks_marks import user_marks_check
from checking.news.get_orioks_news import user_news_check
from checking.homeworks.get_orioks_homeworks import user_homeworks_check
from checking.requests.get_orioks_requests import user_requests_check
from utils.notify_to_user import notify_admins


async def make_one_user_check(user_telegram_id: int) -> set:
    user_notify_settings = db.get_user_notify_settings_to_dict(user_telegram_id=user_telegram_id)
    users_to_one_more_check = set()
    if user_notify_settings['marks']:
        if not await user_marks_check(user_telegram_id=user_telegram_id):
            users_to_one_more_check.add(user_telegram_id)
    if user_notify_settings['news']:
        await user_news_check(user_telegram_id=user_telegram_id)
    if user_notify_settings['discipline_sources']:
        pass  # user_discipline_sources_check(user_telegram_id=user_telegram_id)
    if user_notify_settings['homeworks']:
        if not await user_homeworks_check(user_telegram_id=user_telegram_id):
            users_to_one_more_check.add(user_telegram_id)
    if user_notify_settings['requests']:
        if not await user_requests_check(user_telegram_id=user_telegram_id):
            users_to_one_more_check.add(user_telegram_id)
    return users_to_one_more_check


async def do_checks():
    users_to_check = db.select_all_orioks_authenticated_users()
    users_to_one_more_check = set()
    for user_telegram_id in users_to_check:
        users_to_one_more_check = await make_one_user_check(user_telegram_id=user_telegram_id)
    for user_telegram_id in users_to_one_more_check:
        await make_one_user_check(user_telegram_id=user_telegram_id)


async def scheduler():
    await notify_admins(message='Бот запущен!')
    aioschedule.every(50).seconds.do(do_checks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
