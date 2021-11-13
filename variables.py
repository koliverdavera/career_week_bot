from telebot import types

default_balance = 2
promo_codes = {}  # промокод: количество активаций (от 0 до 5)
STUDENTS = dict()  # {chat_id студента: Student}
REG, GIVE_PROMO, ENTER_PROMO, READY, CHANGE_REG_1, CHANGE_REG_2 = range(6)
mail_pattern = '[a-zA-Z0-9\-]{3,25}@(gmail|mail|ya|yandex|yahoo|outlook|hse|edu\.hse|)\.(ru|net|com|ua)'

companies = {"L'Oreal": "L'Oreal - мировой производитель косметики",
             'Navicon': "Accenture - глобальная консалтинговая компания, один из лидеров мирового рынка "
                        "профессиональных услуг "
                        "и цифровых технологий. Accenture является одной из 500 крупнейших компаний мира (15 лет в "
                        "рейтинге Fortune's Global 500).",
             'FM Logistic': 'FM Logistic – это французская семейная компания, пришедшая на российский рынок более 20 '
                            'лет назад. Энтузиазм и увлеченность своей работой помогли сотрудникам в количестве '
                            'всего 20 человек решиться на открытие бизнеса в России. Эти первопроходцы, преодолев '
                            'создаваемые разностью культур трудности и пережив экономически напряженные времена, '
                            'привели FM Logistic к вершине рынка.\nТеперь компания превратилась в крупнейшего 3PL'
                            ' оператора, постоянно внедряющего ценные инновации и оказывающего полный спектр услуг в '
                            'сфере управления цепью поставок: складирование, копакинг, внутренние перевозки и Global '
                            'Forwarding. На сегодняшний день основными клиентами компании являются сети розничной '
                            'торговли, производители товаров повседневного спроса, косметики, электроники, бытовой '
                            'техники, а также продукции здравоохранения. FM Logistic располагает складскими '
                            'комплексами общей площадью 778 842 м2 по всей России, и это не предел.',
             'Банк Открытие': 'Банк «Открытие» — один из ведущих независимых российских игроков на инвестиционном '
                              'рынке. Предлагаем весь спектр инвестиционно-банковских услуг корпоративным клиентам: '
                              'работа на рынках капитала, операции РЕПО и индивидуальные структурные решения.'}
events = f"🔺Вебинар с L'Oreal\n\n🔹22 ноября 2021 года\n🔹12:00\n🔹https://events.webinar.ru/gsbhse/9586415\n\n\n" \
         f"🔺Завтрак с Navicon\n\n🔹 22 ноября 2021 года\n🔹13:00\n🔹Ссылка появится позже!\n\n\n" \
         f"🔺Вебинар с FM Logistic\n\n🔹 22 ноября 2021 года\n🔹14:00\n🔹Ссылка появится позже!\n\n\n" \
         f"🔺Вебинар с Deloitte & Touche CIS\n\n🔹 22 ноября 2021 года\n🔹15:00\n🔹Ссылка появится позже!\n\n\n"

info = 'Неделя Карьеры ВШБ проводится на нашем факультете весной и осенью. В этот раз она пройдет с 22 по 23 ноября ' \
       '2021 года. В рамках мероприятия состоится 14 вебинаров на самые разные темы.\n\nУ каждого ' \
       'зарегистрированного в боте участника будет свой виртуальный счет с валютой ВШБ - коинами. Проявляя ' \
       'активность на вебинарах, ты сможешь заработать больше коинов. По окончании Недели Карьеры ты сможешь ' \
       'обменять их на мерч Высшей Школы Бизнеса. \n\nС помощью бота ты можешь отслеживать свой баланс, смотреть ' \
       'актуальную' \
       ' программу мероприятий и регистрироваться на них, а также читать информацию компаниях-партнерах ВШБ!\n\n'

welcome = "Привет! Я твой виртуальный помощник на осенней Неделе Карьеры ВШБ.\n\n" + info + 'Для начала работы ' \
                                                                                     'нужно зарегистрироваться. ' \
                                                                                     'Введи, пожалуйста, свои ФИО: '
about_coins = 'После регистрации тебе доступно {} коина.'.format(default_balance)
help_message = 'По вопросам вопросам, связанным с Неделей Карьеры, пиши на почту careers@hse.ru\n' \
               'По вопросам работы с ботом обращайся к @koli_vera '

keyboard_back_menu = types.InlineKeyboardMarkup()
keyboard_back_menu.add(types.InlineKeyboardButton('В меню', callback_data='menu'))

keyboard_back = types.InlineKeyboardMarkup()
keyboard_back.add(types.InlineKeyboardButton('Назад', callback_data='menu'))

keyboard_changes = types.InlineKeyboardMarkup(row_width=2)
b1 = types.InlineKeyboardButton(text='Да', callback_data='changes_needed')
b2 = types.InlineKeyboardButton(text='Нет', callback_data='no_changes_needed')
keyboard_changes.add(b1, b2)

keyboard_companies = types.InlineKeyboardMarkup(row_width=2)
buttons = []
for key, val in companies.items():
    new_button = types.InlineKeyboardButton(text=key, callback_data=key)
    buttons.append(new_button)
keyboard_companies.add(*buttons)
keyboard_companies.add(types.InlineKeyboardButton(text='Назад', callback_data='menu'))

keyboard_change_reg = types.InlineKeyboardMarkup()
b1 = types.InlineKeyboardButton(text='Изменить ФИО', callback_data='change_fio')
b2 = types.InlineKeyboardButton(text='Изменить email', callback_data='change_email')
keyboard_change_reg.add(b1, b2)

keyboard_promo = types.InlineKeyboardMarkup(row_width=2)
keyboard_promo.add(types.InlineKeyboardButton(text='Да', callback_data='activate_promo'),
                   types.InlineKeyboardButton(text='Нет', callback_data='skip_activate_promo'))

keyboard_menu = types.InlineKeyboardMarkup(row_width=1)
b1 = types.InlineKeyboardButton(text='Посмотреть календарь вебинаров', callback_data='event_calendar')
b2 = types.InlineKeyboardButton(text='Посмотреть список работодателей', callback_data='companies')
b3 = types.InlineKeyboardButton(text='Посмотреть свой баланс', callback_data='balance')
b4 = types.InlineKeyboardButton(text='Активировать промокод', callback_data='activate_promo')
b5 = types.InlineKeyboardButton(text='Информация о боте и Неделе Карьеры', callback_data='info')
b6 = types.InlineKeyboardButton(text='Посмотреть данные профиля', callback_data='change_reg')
keyboard_menu.add(b1, b2, b3, b4, b5, b6)
