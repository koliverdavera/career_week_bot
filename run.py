import telebot
from telebot import types
from config import *
from functions import *
from classes import Student

bot = telebot.TeleBot(TOKEN)
keyboard_back = types.InlineKeyboardMarkup()
keyboard_back.add(types.InlineKeyboardButton('Назад', callback_data='menu'))


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я твой виртуальный помощник на осенней Неделе Карьеры ВШБ. "
                                      "Для начала работы нужно зарегистрироваться. Введи, пожалуйста, свои ФИО "
                                      "полностью:", reply_markup=types.ReplyKeyboardRemove())
    print(message.from_user.username)
    bot.register_next_step_handler(message, reg_name)


def reg_name(message):
    fio = message.text
    if not check_name(fio):
        bot.send_message(message.chat.id, 'Пожалуйста, введи ФИО еще раз в корректном формате!')
        bot.register_next_step_handler(message, reg_name)
        return
    fio = message.text
    new_student = Student(fio)
    STUDENTS[message.chat.id] = new_student
    bot.send_message(message.chat.id, 'Теперь введи электронную почту, с которой будешь регистрироваться'
                                      ' на вебинары Недели Карьеры:')
    update_phase(message, EMAIL)
    bot.register_next_step_handler(message, reg_email)


@bot.message_handler(func=lambda message: get_phase(message) == EMAIL)
def reg_email(message):
    a = check_email(message.text)
    if not a:
        bot.send_message(message.chat.id, 'Пожалуйста, введи корректную почту!')
        a = check_email(message.text)
        return
    bot.send_message(message.chat.id, 'Во время Недели Карьеры действует валюта ВШБ - коины. Их можно обменивать на'
                                      ' мерч. Чтобы заработать коины, нужно участвовать в вебинарах и проявлять '
                                      'активность. После регистрации тебе доступно {} коинов.'.format(default_balance))
    STUDENTS[message.chat.id].email = message.text
    update_phase(message, PROMO)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='activate_promo'),
                 types.InlineKeyboardButton(text='Нет', callback_data='skip_activate_promo'))
    bot.send_message(message.chat.id, 'У тебя есть промокод от других участников Недели Карьеры?',
                     reply_markup=keyboard)


@bot.message_handler(func=lambda message: get_phase(message) == PROMO)
def new_promo(message):
    new_code = new_promo_code(message)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Дальше', callback_data='menu'))
    bot.send_message(message.chat.id, f'Это твой уникальный промокод. Если другой участник при регистрации его'
                                      f' активирует, ты получишь 50 коинов. Промокод действителен на 5 применений:\n\n')
    bot.send_message(message.chat.id, f'*{new_code}*', reply_markup=kb, parse_mode="Markdown")
    update_phase(message, READY)


def activate_promo(message):
    code = message.text
    if code not in promo_codes.keys():
        if code == 'menu' or code == 'Меню':
            return
        bot.send_message(message.chat.id, 'Введенный промокод недействителен! Попробуй ввести другой',
                         reply_markup=keyboard_back)
        bot.register_next_step_handler(message, activate_promo)
        return
    promo_codes[code][1] = True
    STUDENTS[message.chat.id].balance += 50
    bot.send_message(message.chat.id, 'Промокод успешно активирован! На твой счет зачислено 50 коинов')


@bot.message_handler(func=lambda message: message.text == 'Меню')
@bot.message_handler(func=lambda message: get_phase(message) == READY)
def menu(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton(text='Посмотреть календарь вебинаров', callback_data='event_calendar')
    b2 = types.InlineKeyboardButton(text='Посмотреть список работодателей', callback_data='companies')
    b3 = types.InlineKeyboardButton(text='Посмотреть свой баланс', callback_data='balance')
    b4 = types.InlineKeyboardButton(text='Активировать промокод', callback_data='activate_promo')
    b5 = types.InlineKeyboardButton(text='Информация о боте и Неделе Карьеры', callback_data='info')
    keyboard.add(b1, b2, b3, b4, b5)
    bot.send_message(message.chat.id, 'Что ты хочешь сделать?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == PROMO)
def is_promo_needed(call):
    if call.data == 'activate_promo':
        bot.send_message(call.message.chat.id, 'Введи твой промокод:')
        bot.register_next_step_handler(call.message, activate_promo)
    elif call.data == 'skip_activate_promo':
        new_promo(call.message)
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def handle_back(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'{call.message.text}',
                          reply_markup=None, parse_mode="Markdown")
    menu(call.message)
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == READY)
def handle_menu(call):
    if call.data == 'event_calendar':
        data = event_calendar()
        res = ''
        for key, val in data.items():
            res += f'{key} состоится {val[0]} по ссылке *{val[1]}*' + '\n'
        bot.send_message(call.message.chat.id, res, parse_mode="Markdown", reply_markup=keyboard_back)
    elif call.data == 'companies':
        data = companies_list()
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for key, val in data.items():
            new_button = types.InlineKeyboardButton(text=key, callback_data=key)
            keyboard.add(new_button)
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='menu'))
        bot.send_message(call.message.chat.id, 'Вот список компаний, сотрудничающих с ВШБ на осенней Неделе Карьеры. '
                                               'Нажмите на кнопку, чтобы почитать про компанию подробнее. ',
                         reply_markup=keyboard)
    elif call.data == 'balance':
        ans = STUDENTS[call.message.chat.id].get_balance()
        bot.send_message(call.message.chat.id, ans, reply_markup=keyboard_back)
    elif call.data == 'activate_promo':
        bot.send_message(call.message.chat.id, 'Введи промокод:')
        bot.register_next_step_handler(call.message, activate_promo)
    elif call.data == 'info':
        bot.send_message(call.message.chat.id, info, reply_markup=keyboard_back)
    elif call.data in companies.keys():
        for key, val in companies_list().items():
            if call.data == key:
                bot.send_message(call.message.chat.id, val, reply_markup=keyboard_back)
                break
    bot.answer_callback_query(callback_query_id=call.id)


@bot.message_handler(content_types='text', func=lambda message: get_phase(message) != PROMO)
def handle_wrong_text(message):
    bot.send_message(message.chat.id, 'Пожалуйста, воспользуйтесь кнопками меню:')
    menu(message)



bot.infinity_polling()
