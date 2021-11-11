from functions import *


class Student:
    def __init__(self, fio):
        self.fio = fio
        self.email = None
        self.balance = 2000
        self.promo_code = False    # ввел ли студент промокод
        self.phase = START

    def get_balance(self):
        return f'Твой баланс составляет {self.balance} коинов. Участвуй в вебинарах и проявляй активность, ' \
               f'чтобы заработать больше.'

    def __repr__(self):
        return f'{self.fio}, {self.email}, {self.balance}, {self.promo_code}'

    # def enter_promo_code(self, promo_code):
    #     # предлагаем ввести существующий промокод от друга
    #     if promo_code in promo_codes.keys():
    #         self.promo_code = True
    #         self.balance += 50 # активация промокода
    #         return True
    #     else:
    #         return False


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

