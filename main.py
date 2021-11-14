import telebot
from data.config import *
from functions import *
from variables import *
import os
from data.database import DATABASE_NAME, create_db

bot = telebot.TeleBot(TOKEN)


# @bot.callback_query_handler(func=lambda call: not get_phase(call.message))
# def handle_none_type(call):
#     menu(call.message)


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in update_students().keys():
        bot.send_message(message.chat.id, 'Ты уже зарегистрировался! Хочешь внести изменения в свой профиль?',
                         reply_markup=keyboard_changes)
        update_phase(message, CHANGE_REG_1)
        return
    bot.send_message(message.chat.id, welcome, parse_mode='MarkDown')
    print(f'Пользователь {message.from_user.username} запустил бота')
    bot.register_next_step_handler(message, reg_name)


def reg_name(message):
    if not check_name(message):
        bot.send_message(message.chat.id, 'Пожалуйста, введи ФИО еще раз в корректном формате!')
        bot.register_next_step_handler(message, reg_name)
        return
    fio = message.text
    new_student = Student(message.chat.id, fio, message.from_user.username)
    Session.add(new_student)
    bot.send_message(message.chat.id, 'Теперь введи электронную почту, с которой будешь регистрироваться'
                                      ' на вебинары Недели Карьеры:')
    bot.register_next_step_handler(message, reg_email)


@bot.message_handler(func=lambda message: get_phase(message) == REG)
def reg_email(message):
    if not check_email(message):
        bot.delete_message(message.chat.id, message_id=message.id)
        bot.send_message(message.chat.id, 'Пожалуйста, введи корректную почту!')
        bot.register_next_step_handler(message, reg_email)
        return
    bot.send_message(message.chat.id, about_coins)
    Session.query(Student).get(message.chat.id).email = message.text
    print(f'Зарегистрирован: {Session.query(Student).get(message.chat.id)}')
    update_phase(message, GIVE_PROMO)
    bot.send_message(message.chat.id, 'У тебя есть промокод от других участников Недели Карьеры? При его активации ты '
                                      'получишь 5 коинов.',
                     reply_markup=keyboard_promo)


def activate_promo(message):
    if get_phase(message) != ENTER_PROMO:
        update_phase(message, READY)
        bot.register_next_step_handler(message, menu)
        return
    code = message.text
    if code not in update_promo_codes():
        if code == 'menu' or code == 'Меню':
            return
        bot.send_message(message.chat.id, 'Введенный промокод недействителен! Попробуй ввести другой',
                         reply_markup=keyboard_back)
        bot.register_next_step_handler(message, activate_promo)
    elif code == Session.query(Student).get(message.chat.id).promo_code:
        bot.send_message(message.chat.id, 'Ты не можешь активировать промокод, выданный тебе :(',
                         reply_markup=keyboard_back)
    else:
        notify = Session.query(Student).filter(Student.promo_code == message.text).first()
        bot.send_message(notify.chat_id, 'Другой пользователь активировал твой промокод! На твой счет зачислено '
                                         '5 коинов :)', reply_markup=keyboard_menu)
        notify.activations += 1
        notify.balance += 5
        Session.query(Student).get(message.chat.id).balance += 5
        Session.query(Student).get(message.chat.id).entered_promo_code = True
        bot.send_message(message.chat.id, 'Промокод успешно активирован! На твой счет зачислено 5 коинов',
                         reply_markup=keyboard_menu)
        update_phase(message, READY)


@bot.message_handler(func=lambda message: get_phase(message) == GIVE_PROMO)
def new_promo(message):
    bot.send_message(message.chat.id, f'Ты успешно зарегистрирован! Вот твой уникальный промокод. Если другой '
                                      f'участник Недели Карьеры при регистрации его '
                                      f' активирует, ты получишь 5 коинов.\nПриглашай друзей участвовать в '
                                      f'осенней Неделе Карьеры ВШБ! Промокод действителен на 5 применений:')
    bot.send_message(message.chat.id, f'*{Session.query(Student).get(message.chat.id).promo_code}*',
                     parse_mode="Markdown", reply_markup=keyboard_back_menu)
    update_phase(message, READY)


@bot.message_handler(func=lambda message: get_phase(message) == READY)
def handle_wrong_text(message):
    bot.send_message(message.chat.id, 'Пожалуйста, воспользуйтесь кнопками меню:')
    menu(message)


@bot.message_handler(func=lambda message: message.text == 'Меню')
def menu(message):
    try:
        if Session.query(Student).get(message.chat.id).entered_promo_code:
            bot.send_message(message.chat.id, 'Что ты хочешь сделать?', reply_markup=keyboard_menu_light)
        else:
            bot.send_message(message.chat.id, 'Что ты хочешь сделать?', reply_markup=keyboard_menu)
    except AttributeError:
        bot.send_message(message.chat.id, 'Что ты хочешь сделать?', reply_markup=keyboard_menu)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == GIVE_PROMO or call.data == 'activate_promo')
def is_promo_needed(call):
    if Session.query(Student).get(call.message.chat.id).entered_promo_code:
        bot.send_message(call.message.chat.id, 'Ты уже активировал промокод!', reply_markup=keyboard_back)
        return
    if call.data == 'activate_promo':
        bot.send_message(call.message.chat.id, 'Введи твой промокод:')
        update_phase(call.message, ENTER_PROMO)
        bot.register_next_step_handler(call.message, activate_promo)
    elif call.data == 'skip_activate_promo':
        new_promo(call.message)
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def handle_back(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'{call.message.text}',
                          reply_markup=None, parse_mode="Markdown")
    update_phase(call.message, READY)
    menu(call.message)
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == READY)
def handle_menu(call):
    if call.data == 'event_calendar':
        bot.send_message(call.message.chat.id, event_calendar_str(), parse_mode="Markdown", reply_markup=keyboard_back)
    elif call.data == 'companies':
        bot.send_message(call.message.chat.id, 'Вот список компаний, сотрудничающих с ВШБ на осенней Неделе Карьеры. '
                                               'Нажмите на кнопку, чтобы почитать про компанию подробнее. ',
                         reply_markup=keyboard_companies)
    elif call.data == 'balance':
        ans = Session.query(Student).get(call.message.chat.id).get_balance()
        bot.send_message(call.message.chat.id, ans, reply_markup=keyboard_back)
    elif call.data == 'info':
        bot.send_message(call.message.chat.id, info, reply_markup=keyboard_back, parse_mode='MarkDown')
    elif call.data in companies_dict().keys():
        for key, val in companies_dict().items():
            if call.data == key:
                bot.send_message(call.message.chat.id, val, reply_markup=keyboard_back)
                break
    elif call.data == 'change_reg':
        bot.send_message(call.message.chat.id, f"Данные твоего профиля сейчас:\n\n"
                                               f"Твои ФИО:\n*{Session.query(Student).get(call.message.chat.id).fio}*\n\n"
                                               f"Твоя электронная почта:\n*{Session.query(Student).get(call.message.chat.id).email}*"
                                               f"\n\nОбрати внимание, что твоя почта должна совпадать с той, с которой "
                                               f"ты будешь регистрироваться на вебинары Недели Карьеры. В противном "
                                               f"случае мы не сможем начислить тебе коины :(", parse_mode='MarkDown')
        bot.send_message(call.message.chat.id, 'Ты хочешь отредактировать свой профиль?',
                         reply_markup=keyboard_changes)
        update_phase(call.message, CHANGE_REG_1)
    else:
        bot.send_message(call.message.chat.id, 'Пожалуйста, воспользуйтесь кнопками меню:')
        menu(call.message)
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == CHANGE_REG_1)
def check_reg(call):
    if call.data == 'changes_needed':
        update_phase(call.message, CHANGE_REG_2)
        bot.send_message(call.message.chat.id, 'Что ты хочешь изменить?', reply_markup=keyboard_change_reg)
    elif call.data == 'no_changes_needed':
        update_phase(call.message, READY)
        bot.send_message(call.message.chat.id, 'Изменения не внесены.', reply_markup=keyboard_back_menu)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'{call.message.text}',
                          reply_markup=None, parse_mode="Markdown")
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: get_phase(call.message) == CHANGE_REG_2)
def change_reg(call):
    if call.data == 'change_fio':
        new_name(call.message)
    elif call.data == 'change_email':
        new_email(call.message)
    bot.answer_callback_query(callback_query_id=call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'{call.message.text}',
                          reply_markup=None, parse_mode="Markdown")


@bot.message_handler(
    content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                   "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                   "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                   "migrate_from_chat_id", "pinned_message"])
def send_sticker(message):
    sticker = open('./sticker_hse.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)


def create_database():
    create_db()


if __name__ == '__main__':
    set_env_functions(bot)
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_database()
    print('vvf')
    bot.infinity_polling(timeout=None)
