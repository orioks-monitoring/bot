from aiogram import types
from aiogram.utils import markdown

from app.handlers import AbstractCommandHandler
from app.keyboards.authorization import AuthorizationReplyKeyboard


class OrioksAuthCancelCommandHandler(AbstractCommandHandler):
    @staticmethod
    async def process(message: types.Message, *args, **kwargs):
        state = kwargs.get('state', None)

        current_state = await state.get_state()
        if current_state is None:
            return

        await state.finish()
        await message.reply(
            markdown.text(
                markdown.hbold('Авторизация отменена.'),
                markdown.text(
                    'Если ты боишься вводить свои данные, ознакомься со следующей <a href="https://orioks-monitoring.github.io/bot/faq#почему-это-безопасно">информацией</a>'
                ),
                sep='\n',
            ),
            reply_markup=await AuthorizationReplyKeyboard.show(),
            disable_web_page_preview=True,
        )
