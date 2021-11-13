from variables import *
import re
from classes import Student


def set_env_functions(real_bot):
    global bot
    bot = real_bot


def reg_name(message):
    if not check_name(message):
        bot.delete_message(message.chat.id, message_id=message.id)
        bot.send_message(message.chat.id, 'Пожалуйста, введи ФИО еще раз в корректном формате!')
        bot.register_next_step_handler(message, reg_name)
        return
    fio = message.text
    new_student = Student(fio, message)
    STUDENTS[message.chat.id] = new_student
    bot.send_message(message.chat.id, 'Теперь введи электронную почту, с которой будешь регистрироваться'
                                      ' на вебинары Недели Карьеры:')
    bot.register_next_step_handler(message, reg_email)


def new_name(message):
    if message.text == 'Что ты хочешь изменить?':
        bot.send_message(message.chat.id, 'Введи корректные ФИО:')
        bot.register_next_step_handler(message, new_name)
        return
    if not check_name(message):
        bot.delete_message(message.chat.id, message_id=message.id)
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
        bot.delete_message(message.chat.id, message_id=message.id)
        bot.send_message(message.chat.id, 'Пожалуйста, введи корректную почту!')
        bot.register_next_step_handler(message, new_email)
        return
    STUDENTS[message.chat.id].email = message.text
    update_phase(message, READY)
    bot.send_message(message.chat.id, 'Данные успешно обновлены!', reply_markup=keyboard_back_menu)


def activate_promo(message):
    if get_phase(message) != ENTER_PROMO:
        update_phase(message, READY)
        bot.register_next_step_handler(message, menu)
        return
    code = message.text
    if code not in promo_codes.keys():
        if code == 'menu' or code == 'Меню':
            return
        bot.send_message(message.chat.id, 'Введенный промокод недействителен! Попробуй ввести другой',
                         reply_markup=keyboard_back)
        bot.register_next_step_handler(message, activate_promo)
    elif STUDENTS[message.chat.id].bool_promo_code:
        bot.send_message(message.chat.id, 'Ты уже активировал промокод!', reply_markup=keyboard_back)
        return
    elif code == STUDENTS[message.chat.id].given_promo_code:
        bot.send_message(message.chat.id, 'Ты не можешь активировать промокод, выданный тебе :(',
                         reply_markup=keyboard_back)
    else:
        promo_codes[code] += 1
        STUDENTS[message.chat.id].balance += 50
        print(STUDENTS)
        STUDENTS[message.chat.id].bool_promo_code = True
        bot.send_message(message.chat.id, 'Промокод успешно активирован! На твой счет зачислено 50 коинов')
        update_phase(message, READY)


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

