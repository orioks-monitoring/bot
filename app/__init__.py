import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from prometheus_client import start_http_server
from sqlalchemy.orm.scoping import ScopedSession

from app.logging import setup_logging
from config import config


def initialize_database() -> ScopedSession:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    engine = create_engine(config.DATABASE_URL, convert_unicode=True)
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def _settings_before_start() -> None:
    from app.fixtures import initialize_default_values
    from app.handlers import register_handlers
    from app.middlewares import (
        AdminCommandsMiddleware,
        PrometheusMiddleware,
        UserAgreementMiddleware,
        UserOrioksAttemptsMiddleware,
    )

    register_handlers(dispatcher=dispatcher)
    initialize_default_values()
    dispatcher.middleware.setup(UserAgreementMiddleware())
    dispatcher.middleware.setup(UserOrioksAttemptsMiddleware())
    dispatcher.middleware.setup(AdminCommandsMiddleware())
    dispatcher.middleware.setup(PrometheusMiddleware())


bot = Bot(token=config.TELEGRAM_BOT_API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)

db_session = initialize_database()


async def on_startup(_) -> None:
    from app.helpers import MessageToAdminsHelper

    await MessageToAdminsHelper.send("Bot запущен")


async def on_shutdown(_) -> None:
    from app.helpers import MessageToAdminsHelper

    await MessageToAdminsHelper.send("Bot остановлен!")


def run():
    setup_logging()
    _settings_before_start()
    start_http_server(8880)
    executor.start_polling(
        dispatcher,
        skip_updates=False,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )
