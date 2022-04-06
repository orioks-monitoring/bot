from aiogram.utils.exceptions import ChatNotFound, BotBlocked
import main
import config
import utils.handle_orioks_logout
import aiogram.utils.markdown as md


async def notify_admins(message: str) -> None:
    for admin_telegram_id in config.TELEGRAM_ADMIN_IDS_LIST:
        await main.bot.send_message(
            admin_telegram_id,
            md.text(
                md.hbold('[ADMIN]'),
                md.text(message),
                sep=': ',
            )
        )


async def notify_user(user_telegram_id: int, message: str) -> None:
    try:
        await main.bot.send_message(user_telegram_id, message)
    except (BotBlocked, ChatNotFound) as e:
        utils.handle_orioks_logout.make_orioks_logout(user_telegram_id=user_telegram_id)
