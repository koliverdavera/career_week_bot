from variables import *
import re
from classes import Student


def set_env_functions(real_bot):
    global bot
    bot = real_bot


def new_name(message):
    if message.text == 'Что ты хочешь изменить?':
        bot.send_message(message.chat.id, 'Введи корректные ФИО:')
        bot.register_next_step_handler(message, new_name)
        return
    if not check_name(message):
        bot.send_message(message.chat.id, 'Пожалуйста, введи ФИО еще раз в корректном формате!')
        bot.register_next_step_handler(message, new_name)
        return
    bot.send_message(message.chat.id, 'Данные успешно обновлены!', reply_markup=keyboard_back_menu)
    STUDENTS[message.chat.id].fio = message.text
    update_phase(message, READY)


def new_email(message):
    if message.text == 'Что ты хочешь изменить?':
        bot.send_message(message.chat.id, 'Введи корректную электронную почту:')
        bot.register_next_step_handler(message, new_email)
        return
    if not check_email(message):
        bot.send_message(message.chat.id, 'Пожалуйста, введи корректную почту!')
        bot.register_next_step_handler(message, new_email)
        return
    STUDENTS[message.chat.id].email = message.text
    update_phase(message, READY)
    bot.send_message(message.chat.id, 'Данные успешно обновлены!', reply_markup=keyboard_back_menu)


def get_phase(message):
    return STUDENTS[message.chat.id].phase


def update_phase(message, new_phase):
    STUDENTS[message.chat.id].phase = new_phase


def check_email(message):
    if re.fullmatch(mail_pattern, message.text):
        return True
    return False


def check_name(message):
    if message.content_type != 'text':
        return False
    name = message.text
    return check_name_name(name)


def check_name_name(name):
    if not 2 <= len(name.split()) <= 3:
        return False
    for symb in name:
        if symb.isdigit():
            return False
    return True


def event_calendar():
    return events


def companies_list():
    return companies

