from sqlalchemy import Column, Integer, String, BOOLEAN
from data.database import Base
import random
from variables import *


def generate_code(length=8):
    alphabet = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    code = ''
    for _ in range(length):
        code += alphabet[random.randint(0, len(alphabet) - 1)]
    return code


class Student(Base):
    __tablename__ = 'students'

    chat_id = Column(Integer, primary_key=True)    #primary_key => первичный ключ
    fio = Column(String)
    user_name = Column(String)
    email = Column(String)
    balance = Column(Integer)
    phase = Column(Integer)
    promo_code = Column(String)
    activations = Column(Integer)
    entered_promo_code = Column(BOOLEAN)

    def __init__(self, chat_id: int, fio: str, user_name: str, email=''):
        self.chat_id = chat_id
        self.fio = fio
        self.user_name = user_name
        self.email = email
        self.balance = default_balance
        self.phase = REG
        self.promo_code = generate_code()
        self.activations = 0
        self.entered_promo_code = False

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
               f'применил ли промокод: {"Да" if self.entered_promo_code else "Нет"}, ' \
               f'выданный промокод: {self.promo_code}, фаза: {self.phase}'

    def change_fio(self, new_fio):
        self.fio = new_fio
