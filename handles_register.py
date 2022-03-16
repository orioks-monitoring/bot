from forms import Form
from handlers import commands, orioks_auth, notify_settings


def handles_register(dp):
    """commands"""
    dp.register_message_handler(commands.start_cmd_handler, text=['Меню'])
    dp.register_message_handler(commands.start_cmd_handler, commands=['start'])

    dp.register_message_handler(commands.msg_manual, text=['Руководство'])
    dp.register_message_handler(commands.msg_manual, commands=['manual'])

    dp.register_message_handler(commands.msg_faq, text=['О проекте'])
    dp.register_message_handler(commands.msg_faq, commands=['faq'])

    """orioks_auth"""
    dp.register_message_handler(orioks_auth.cmd_start, text=['Авторизация'])
    dp.register_message_handler(orioks_auth.cmd_start, commands=['login'])

    dp.register_message_handler(orioks_auth.orioks_logout, commands=['logout'])

    dp.register_message_handler(orioks_auth.cancel_handler, commands=['cancel'], state='*')

    dp.register_message_handler(orioks_auth.process_login_invalid, lambda message: not message.text.isdigit(),
                                state=Form.login)

    dp.register_message_handler(orioks_auth.process_login, state=Form.login)

    dp.register_message_handler(orioks_auth.process_password, state=Form.password)

    """notify settings"""
    dp.register_message_handler(notify_settings.user_settings, text=['Настройка уведомлений'])
    dp.register_message_handler(notify_settings.user_settings, commands=['notifysettings'])
