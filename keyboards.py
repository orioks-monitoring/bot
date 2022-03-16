from aiogram import types


def main_menu_keyboard(first_btn_text: str) -> types.ReplyKeyboardMarkup:
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard_markup.row(types.KeyboardButton(str(first_btn_text)))

    more_btns_text = ('Руководство', 'О проекте')
    keyboard_markup.add(*(types.KeyboardButton(text) for text in more_btns_text))
    return keyboard_markup
