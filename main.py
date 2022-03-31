import logging
import time

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
