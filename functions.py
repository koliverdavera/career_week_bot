from variables import *
import re
from data.students import Student
from data.events import Event
from data.companies import Company


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
    Session.query(Student).get(message.chat.id).fio = message.text
    Session.commit()
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
    Session.query(Student).get(message.chat.id).email = message.text
    update_phase(message, READY)
    Session.commit()
    bot.send_message(message.chat.id, 'Данные успешно обновлены!', reply_markup=keyboard_back_menu)


def update_students():
    students = Session.query(Student)
    students_dict = dict()
    for it in students:
        students_dict[it.chat_id] = it
    return students_dict


def update_promo_codes():
    stud = update_students()
    promo_codes = []
    for student in stud.values():
        promo_codes.append(student.promo_code)
    return promo_codes


def get_phase(message):
    student = Session.query(Student).get(message.chat.id)
    if student is None:
        return False
    return student.phase


def update_phase(message, new_phase):
    student = Session.query(Student).get(message.chat.id)
    student.phase = new_phase
    Session.commit()


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




