import random
from variables import *


def generate_code(length=8):
    alphabet = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    code = ''
    for _ in range(length):
        code += alphabet[random.randint(0, len(alphabet) - 1)]
    return code


def new_promo_code():
    new_code = generate_code()
    while new_code in promo_codes.keys():
        new_code = generate_code()
    promo_codes[new_code] = 0
    return new_code


def get_phase(message):
    return STUDENTS[message.chat.id].phase


def update_phase(message, new_phase):
    STUDENTS[message.chat.id].phase = new_phase


def check_email(message):
    email = message.text
    counter1, counter2 = 0, 0
    if len(email) < 4:
        return False
    for symb in email:
        if symb in r'!&/\+=><*^%;$#:""''':
            return False
        if symb == '@':
            counter1 += 1
        if symb == '.':
            counter2 += 1
    if counter1 != 1:
        return False
    if counter2 == 0:
        return False
    return True


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

