import aiogram.utils.markdown as md
from aiogram import types

import db.notify_settings
from handlers import notify_settings
from main import bot


async def send_user_settings(user_id: int, callback_query: types.CallbackQuery = None) -> types.Message:
    is_on_off_dict = db.notify_settings.get_user_notify_settings_to_dict(user_telegram_id=user_id)
    text = md.text(
        md.text(
            md.text('📓'),
            md.text(
                md.hbold('“Обучение”'),
                md.text('изменения баллов в накопительно-балльной системе (НБС)'),
                sep=': ',
            ),
            sep=' ',
        ),
        md.text(
            md.text('📰'),
            md.text(
                md.hbold('“Новости”'),
                md.text('публикация общих новостей\n(новости по дисциплинам', md.hitalic('(coming soon))')),
                sep=': ',
            ),
            sep=' ',
        ),
        md.text(
            md.text('📁'),
            md.text(
                md.hbold('“Ресурсы”'),
                md.text('изменения и загрузка файлов по дисциплине', md.hitalic('(coming soon)')),
                sep=': ',
            ),
            sep=' ',
        ),
        md.text(
            md.text('📝'),
            md.text(
                md.hbold('“Домашние задания”'),
                md.text('изменения статусов отправленных работ'),
                sep=': ',
            ),
            sep=' ',
        ),
        md.text(
            md.text('📄'),
            md.text(
                md.hbold('“Заявки”'),
                md.text('изменения статусов заявок на обходной лист, материальную помощь, '
                        'социальную стипендию, копии документов, справки'),
                sep=': ',
            ),
            sep=' ',
        ),
        sep='\n\n',
    )
    if not callback_query:
        return await bot.send_message(
            user_id,
            text=text,
            reply_markup=notify_settings.init_notify_settings_inline_btns(is_on_off=is_on_off_dict),
        )
    return await callback_query.message.edit_text(
        text=text,
        reply_markup=notify_settings.init_notify_settings_inline_btns(is_on_off=is_on_off_dict),
    )
