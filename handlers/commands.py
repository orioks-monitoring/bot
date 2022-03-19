import logging

import aiogram.utils.markdown as md
from aiogram import types

from answers import menu

logger = logging.getLogger(__name__)


async def start_cmd_handler(message: types.Message):
    """"
    @dp.message_handler(text='Меню')
    @dp.message_handler(commands='start')
    """
    await menu.menu_command(chat_id=message.chat.id, user_id=message.from_user.id)


async def msg_manual(message: types.Message):
    """
    @dp.message_handler(text='Руководство')
    @dp.message_handler(commands='manual')
    """
    await message.reply(
        md.text(
            md.text('[manual url]'),
        ),
    )


async def msg_faq(message: types.Message):
    """
    @dp.message_handler(text='О проекте')
    @dp.message_handler(commands='faq')
    """
    await message.reply(
        md.text(
            md.text('[faq url]'),
        ),
    )
