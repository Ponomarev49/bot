import telebot
from telebot import types
from decouple import config
import random

BOT_TOKEN = config('BOT_TOKEN', default='')
bot = telebot.TeleBot(BOT_TOKEN)
first_num = {}
second_num = {}
bid = {}
balance = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Привет!")
    markup.add(btn1)
    balance[message.from_user.id] = 1000
    bot.send_message(message.from_user.id, "👋 Привет! Я могу тебе показать увлекательную игру, с помощью которой ты "
                                           "сможешь запросто убить время.", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global first_num, second_num, balance, bid
    if message.text == '👋 Привет!' or message.text == 'Меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Игра')
        btn2 = types.KeyboardButton('Об авторе')
        btn4 = types.KeyboardButton('Выход')
        markup.add(btn1, btn2, btn4)
        bot.send_message(message.from_user.id, 'Сейчас вы находитесь в главном меню.', reply_markup=markup)

    if message.text == '👋 Привет, Я снова здесь!':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Игра')
        btn2 = types.KeyboardButton('Об авторе')
        btn4 = types.KeyboardButton('Выход')
        markup.add(btn1, btn2, btn4)
        bot.send_message(message.from_user.id, 'Я рад тебя снова видеть!\n'
                                               'Сейчас вы находитесь в главном меню.', reply_markup=markup)

    if message.text == 'Об авторе':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Меню')
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'Я ожил благодаря моим создателям!\n'
                                               'Долго и упорно трудились:\n'
                                               'Студенты ФИТ-221 Черникова Алена и Пономарев Михаил',
                         reply_markup=markup)

    elif message.text == 'Игра':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Играем')
        btn2 = types.KeyboardButton('Меню')
        btn4 = types.KeyboardButton('Об игре')
        markup.add(btn1, btn4, btn2)
        bot.send_message(message.from_user.id, 'Сыграем❓', reply_markup=markup)

    elif message.text == 'Играем' or message.text == 'Сыграть еще' or message.text == 'Сделано!':
        if balance[message.from_user.id] == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Сделано!')
            markup.add(btn1)
            mesg = bot.send_message(message.from_user.id, f'На вашем счету нет средств!\nДля того, чтобы пополнить '
                                                          f'баланс, сделайте 10 отжиманий!',
                                    reply_markup=markup)
            balance[message.from_user.id] += 1000
            bot.register_next_step_handler(mesg, get_text_messages)
        else:
            mesg = bot.send_message(message.from_user.id, f'Ваш баланс - {balance[message.from_user.id]}\n'
                                                          f'Введите размер вашей ставки')
            bot.register_next_step_handler(mesg, game)

    elif message.text == 'Больше >':
        if first_num[message.from_user.id] < second_num[message.from_user.id]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Сыграть еще')
            btn2 = types.KeyboardButton('Меню')
            markup.add(btn1, btn2)
            balance[message.from_user.id] += bid[message.from_user.id] * round(
                99 / (99 - first_num[message.from_user.id]),
                2)
            bot.send_message(message.from_user.id,
                             f'Число 1 - {first_num[message.from_user.id]}\nЧисло 2 - '
                             f'{second_num[message.from_user.id]}\nВы выиграли!\n'
                             f'Ваш баланс - {balance[message.from_user.id]}',
                             reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Сыграть еще')
            btn2 = types.KeyboardButton('Меню')
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id,
                             f'Число 1 - {first_num[message.from_user.id]}\nЧисло 2 - '
                             f'{second_num[message.from_user.id]}\n'
                             f'Вы проиграли!\n'
                             f'Ваш баланс - {balance[message.from_user.id]}',
                             reply_markup=markup)

    elif message.text == 'Равно =':
        if first_num[message.from_user.id] == second_num[message.from_user.id]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Сыграть еще')
            btn2 = types.KeyboardButton('Меню')
            markup.add(btn1, btn2)
            balance[message.from_user.id] += bid[message.from_user.id] * round(99, 2)
            bot.send_message(message.from_user.id,
                             f'Число 1 - {first_num[message.from_user.id]}\nЧисло 2 - '
                             f'{second_num[message.from_user.id]}\nВы выиграли!\n'
                             f'Ваш баланс - {balance[message.from_user.id]}',
                             reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Сыграть еще')
            btn2 = types.KeyboardButton('Меню')
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id,
                             f'Число 1 - {first_num[message.from_user.id]}\nЧисло 2 - '
                             f'{second_num[message.from_user.id]}\nВы проиграли!\n'
                             f'Ваш баланс - {balance[message.from_user.id]}',
                             reply_markup=markup)

    elif message.text == 'Меньше <':
        if first_num[message.from_user.id] > second_num[message.from_user.id]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Сыграть еще')
            btn2 = types.KeyboardButton('Меню')
            markup.add(btn1, btn2)
            balance[message.from_user.id] += bid[message.from_user.id] * round(
                99 / (first_num[message.from_user.id] - 1), 2)
            bot.send_message(message.from_user.id,
                             f'Число 1 - {first_num[message.from_user.id]}\nЧисло 2 - '
                             f'{second_num[message.from_user.id]}\nВы выиграли!\n'
                             f'Ваш баланс - {balance[message.from_user.id]}',
                             reply_markup=markup)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Сыграть еще')
            btn2 = types.KeyboardButton('Меню')
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id,
                             f'Число 1 - {first_num[message.from_user.id]}\nЧисло 2 - '
                             f'{second_num[message.from_user.id]}\nВы проиграли!\n'
                             f'Ваш баланс - {balance[message.from_user.id]}',
                             reply_markup=markup)

    elif message.text == 'Об игре':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Играем')
        btn4 = types.KeyboardButton('Меню')
        markup.add(btn1, btn4)
        bot.send_message(message.from_user.id, 'Цель игры состоит в том, чтобы угадать, будет следующее число '
                                               'большего, меньшего или равного достоинства, чем число, которое уже '
                                               'дано.\n'
                                               'Каждый раз мы умножить свой выигрыш, '
                                               'если правильное угадаете следующее число'
                                               'Цель этой игре получать удовольствие, потому что на данный момент '
                                               'игра не расчита на реальные денежные средства'
                                               'Развлекайтесь!', reply_markup=markup)

    elif message.text == 'Выход':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👋 Привет, Я снова здесь!")
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'До новой встречи!', reply_markup=markup)


def game(message):
    try:
        global first_num, second_num, balance, bid
        bid[message.from_user.id] = float(message.text)
        if bid[message.from_user.id] <= 0:
            mesg = bot.send_message(message.from_user.id, f'Неправильный ввод\n'
                                                          f'Ваш баланс - {balance[message.from_user.id]}\n'
                                                          f'Введите размер вашей ставки')
            bot.register_next_step_handler(mesg, game)

        elif bid[message.from_user.id] > balance[message.from_user.id]:
            bot.send_message(message.from_user.id, f'Недостаточно средств')
            mesg = bot.send_message(message.from_user.id, f'\nВаш баланс - {balance[message.from_user.id]}\n'
                                                          f'Введите размер вашей ставки')
            bot.register_next_step_handler(mesg, game)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Больше >')
            btn2 = types.KeyboardButton('Равно =')
            btn3 = types.KeyboardButton('Меньше <')
            markup.add(btn1, btn2, btn3)
            first_num[message.from_user.id] = random.randint(2, 99)
            second_num[message.from_user.id] = random.randint(1, 99)
            mesg = bot.send_message(message.from_user.id,
                                    f'Ставка принята!\nВаша ставка - {bid[message.from_user.id]}\nЧисло '
                                    f'{first_num[message.from_user.id]}\n'
                                    f'Больше\tx{round(99 / (99 - first_num[message.from_user.id]), 2)}\n'
                                    f'Равно\tx{round(99, 2)}\n'
                                    f'Меньше\tx{round(99 / (first_num[message.from_user.id] - 1), 2)}\t\nВаш выбор?',
                                    reply_markup=markup)
            balance[message.from_user.id] -= bid[message.from_user.id]
            bot.register_next_step_handler(mesg, get_text_messages)
    except ValueError:
        mesg = bot.send_message(message.from_user.id, 'Неправильный ввод')
        bot.register_next_step_handler(mesg, game)


bot.polling(none_stop=True, interval=0)
