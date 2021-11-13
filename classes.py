from variables import *
import datetime
import random


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


class Student:
    def __init__(self, fio, any_message):
        self.fio = fio
        self.user_id = any_message.from_user.id
        self.user_name = any_message.from_user.username
        self.email = None
        self.balance = default_balance
        self.bool_promo_code = False    # ввел ли студент промокод
        self.given_promo_code = generate_code()
        promo_codes[self.given_promo_code] = 0
        self.phase = REG

    def sklonenie(self):
        numb = self.balance % 100
        if numb == 1 or numb % 10 == 1:
            return 'коин'
        if 2 <= numb <= 4:
            return "коина"
        if 5 <= numb <= 20 or numb % 10 != 1:
            return 'коинов'

    def get_balance(self):
        return f'Твой баланс составляет {self.balance} {self.sklonenie()}. Участвуй в вебинарах и проявляй активность, ' \
               f'чтобы заработать больше.'

    def __repr__(self):
        return f'Студент: {self.fio}, почта: {self.email}, баланс: {self.balance}, ' \
               f'применил ли промокод: {"Да" if self.bool_promo_code else "Нет"}, ' \
               f'выданный промокод: {self.given_promo_code}, фаза: {self.phase}'

    def change_fio(self, new_fio):
        self.fio = new_fio


class Company:
    def __init__(self, name, info, balance):
        self.name = name
        self.info = info
        self.balance = balance


class Event:
    def __init__(self, name, date_time, link):
        self.name = name
        self.date_time = date_time
        self.link = link

    def get_event_info(self):
        return f'Мероприятие: {self.name}, дата и время: {datetime.datetime.strftime(self.date_time, "%d %B %H:%M")}'

