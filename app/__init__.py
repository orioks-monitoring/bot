import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from sqlalchemy.orm.scoping import ScopedSession

from config import config


def initialize_database() -> ScopedSession:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    engine = create_engine(config.DATABASE_URL, convert_unicode=True)
    return scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )


def _settings_before_start() -> None:
    from app.handlers import register_handlers
    from app.fixtures import initialize_default_values
    from app.middlewares import (
        UserAgreementMiddleware,
        UserOrioksAttemptsMiddleware,
        AdminCommandsMiddleware,
    )

    register_handlers(dispatcher=dispatcher)
    initialize_default_values()
    dispatcher.middleware.setup(UserAgreementMiddleware())
    dispatcher.middleware.setup(UserOrioksAttemptsMiddleware())
    dispatcher.middleware.setup(AdminCommandsMiddleware())


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
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s - %(module)s - %(funcName)s - %(lineno)d: %(message)s",
        datefmt='%H:%M:%S %d.%m.%Y',
    )
    _settings_before_start()
    executor.start_polling(
        dispatcher,
        skip_updates=False,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )
