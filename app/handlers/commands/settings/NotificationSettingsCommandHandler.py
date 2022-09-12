from aiogram import types
from aiogram.utils import markdown

import app
from app.handlers import AbstractCommandHandler
from app.keyboards.notify_settings import NotifySettingsInlineKeyboard


class NotificationSettingsCommandHandler(AbstractCommandHandler):
    @staticmethod
    async def process(message: types.Message, *args, **kwargs):
        await NotificationSettingsCommandHandler.send_user_settings(
            message.from_user.id, callback_query=None
        )

    @staticmethod
    async def send_user_settings(
        user_id: int, callback_query: types.CallbackQuery = None
    ) -> types.Message:
        text = markdown.text(
            markdown.text(
                markdown.text('📓'),
                markdown.text(
                    markdown.hbold('“Обучение”'),
                    markdown.text(
                        'изменения баллов в накопительно-балльной системе (НБС)'
                    ),
                    sep=': ',
                ),
                sep=' ',
            ),
            markdown.text(
                markdown.text('📰'),
                markdown.text(
                    markdown.hbold('“Новости”'),
                    markdown.text(
                        'публикация общих новостей\n(новости по дисциплинам',
                        markdown.hitalic('(coming soon))'),
                    ),
                    sep=': ',
                ),
                sep=' ',
            ),
            markdown.text(
                markdown.text('📁'),
                markdown.text(
                    markdown.hbold('“Ресурсы”'),
                    markdown.text(
                        'изменения и загрузка файлов по дисциплине',
                        markdown.hitalic('(coming soon)'),
                    ),
                    sep=': ',
                ),
                sep=' ',
            ),
            markdown.text(
                markdown.text('📝'),
                markdown.text(
                    markdown.hbold('“Домашние задания”'),
                    markdown.text('изменения статусов отправленных работ'),
                    sep=': ',
                ),
                sep=' ',
            ),
            markdown.text(
                markdown.text('📄'),
                markdown.text(
                    markdown.hbold('“Заявки”'),
                    markdown.text(
                        'изменения статусов заявок на обходной лист, материальную помощь, '
                        'социальную стипендию, копии документов, справки'
                    ),
                    sep=': ',
                ),
                sep=' ',
            ),
            sep='\n\n',
        )
        if not callback_query:
            return await app.bot.send_message(
                user_id,
                text=text,
                reply_markup=await NotifySettingsInlineKeyboard.show(
                    user_telegram_id=user_id
                ),
            )
        return await callback_query.message.edit_text(
            text=text,
            reply_markup=await NotifySettingsInlineKeyboard.show(
                user_telegram_id=user_id
            ),
        )
