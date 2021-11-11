import random
import datetime


def generate_code(length=8):
    alphabet = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    code = ''
    for _ in range(length):
        code += alphabet[random.randint(0, len(alphabet) - 1)]
    return code


def new_promo_code(message):
    new_code = generate_code()
    while new_code in promo_codes.keys():
        new_code = generate_code()
    promo_codes[new_code] = [message.chat.id, False]
    return new_code


promo_codes = {}   # промокод: [user_id, количество активаций (от 0 до 5)]
STUDENTS = dict()   # {user_id: Student}
START, EMAIL, PROMO, READY = range(4)
default_balance = 2000
companies = {'McKinsey': 'McKinsey - одна из крупнейших консалтинговых компаний в мире',
             "L'Oreal" : "L'Oreal - Мировой производитель косметики",
             'Accenture': "Accenture - глобальная консалтинговая компания, один из лидеров мирового рынка профессиональных услуг "
                          "и цифровых технологий. Accenture является одной из 500 крупнейших компаний мира (15 лет в "
                          "рейтинге Fortune's Global 500)."}
events = {'Вебинар с ВТБ': ['22 ноября в 11.00', 'ссылка на вебинар 1'],
          'Завтрак с McKinsey': ['22 ноября в 12.00', 'ссылка на вебинар 2'],
          'Вебинар о карьерном росте': ['23 ноября в 16.00', 'ссылка на вебинар 3']}
info = 'Неделя Карьеры ВШБ проводится на нашем факультете весной и осенью. В этот раз она пройдет с 22 по 23 ноября ' \
       '2021 года. В рамках мероприятия состоится 14 вебинаров на самые разные темы. \nТакже у каждого ' \
       'зарегистрированного в боте участника будет свой виртуальный счет с валютой ВШБ - коинами. Проявляя активность' \
       ' на вебинарах, ты сможешь заработать больше коинов. По окончании Недели Карьеры ты сможешь обменять их на ' \
       'мерч Высшей Школы Бизнеса.\nС помощью бота ты можешь отслеживать свой баланс, смотреть актуальную программу ' \
       'мероприятий и регистрироваться на них, а также читать информацию компаниях-партнерах ВШБ!'


def get_phase(message):
    return STUDENTS[message.chat.id].phase


def update_phase(message, new_phase):
    STUDENTS[message.chat.id].phase = new_phase


def check_email(email):
    counter1, counter2 = 0, 0
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


def check_name(name):
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

