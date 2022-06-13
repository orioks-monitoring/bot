import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import utils.makedirs

from app.handlers import register_handlers
from app.middlewares import UserAgreementMiddleware, UserOrioksAttemptsMiddleware, AdminCommandsMiddleware
from checking import on_startup

from config import Config

import db.admins_statistics

bot = Bot(token=Config.TELEGRAM_BOT_API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def _settings_before_start() -> None:
    register_handlers(dispatcher=dispatcher)
    db.admins_statistics.create_and_init_admins_statistics()
    dispatcher.middleware.setup(UserAgreementMiddleware())
    dispatcher.middleware.setup(UserOrioksAttemptsMiddleware())
    dispatcher.middleware.setup(AdminCommandsMiddleware())
    utils.makedirs.make_dirs()
    pass


def run():
    logging.basicConfig(level=logging.INFO)
    _settings_before_start()
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup.on_startup)
