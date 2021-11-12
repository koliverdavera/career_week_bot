from variables import *
from functions import generate_code
import datetime


class Student:
    def __init__(self, fio):
        self.fio = fio
        self.email = None
        self.balance = default_balance
        self.bool_promo_code = False    # ввел ли студент промокод
        self.given_promo_code = generate_code()
        self.phase = REG

    def get_balance(self):
        return f'Твой баланс составляет {self.balance} коинов. Участвуй в вебинарах и проявляй активность, ' \
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

