import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

import answers
import config

import db.user_status
import db.notify_settings
import db.admins_statistics

import handles_register
import middlewares
from checking import on_startup
import utils.makedirs

bot = Bot(token=config.TELEGRAM_BOT_API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.callback_query_handler(lambda c: c.data == 'button_user_agreement_accept')
async def callback_query_handler_user_agreement(callback_query: types.CallbackQuery):
    if db.user_status.get_user_agreement_status(user_telegram_id=callback_query.from_user.id):
        return await bot.answer_callback_query(
            callback_query.id,
            text='Пользовательское соглашение уже принято.', show_alert=True)
    db.user_status.update_user_agreement_status(
        user_telegram_id=callback_query.from_user.id,
        is_user_agreement_accepted=True
    )
    await bot.answer_callback_query(callback_query.id)
    answer_message = await bot.send_message(callback_query.from_user.id, 'Пользовательское соглашение принято!')
    await answers.menu.menu_command(chat_id=answer_message.chat.id, user_id=callback_query.from_user.id)


@dp.callback_query_handler(lambda c: c.data in config.notify_settings_btns)
async def callback_query_handler_notify_settings_btns(callback_query: types.CallbackQuery):
    _row_name = callback_query.data.split('-')[1]
    if callback_query.data in ['notify_settings-discipline_sources']:
        return await bot.answer_callback_query(
            callback_query.id,
            text='Эта категория ещё недоступна.', show_alert=True
        )
    db.notify_settings.update_user_notify_settings(
        user_telegram_id=callback_query.from_user.id,
        row_name=_row_name,
        to_value=not db.notify_settings.get_user_notify_settings_to_dict(user_telegram_id=callback_query.from_user.id)[_row_name],
    )
    sent = await answers.settings.send_user_settings(user_id=callback_query.from_user.id)
    await bot.delete_message(chat_id=sent.chat.id, message_id=sent.message_id - 1)


def _settings_before_start() -> None:
    handles_register.handles_register(dp)
    db.admins_statistics.create_and_init_admins_statistics()
    dp.middleware.setup(middlewares.UserAgreementMiddleware())
    dp.middleware.setup(middlewares.UserOrioksAttemptsMiddleware())
    dp.middleware.setup(middlewares.AdminCommandsMiddleware())
    utils.makedirs.make_dirs()


def main():
    logging.basicConfig(level=logging.INFO)
    _settings_before_start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup.on_startup)


if __name__ == '__main__':
    main()
