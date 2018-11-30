from json import loads

from requests import get
from telebot import types
from telebot import TeleBot

token = "767108584:AAGXsYsu_gqX1Be3O-p98fa8WwlR5QYyHMI"
bot = TeleBot(token)


@bot.message_handler(func=lambda message: message.text == "Return last games", content_types='text')
def return_last_games(message):
    games = get('https://test.bop.rest/api/feed/',
                headers={'Authorization': 'Token 233e7ef7888d82e098b3d63ca2a888d0e32a0eea'}).content

    for game in loads(games)[-10:]:
        datetime = game['time'].split('T')

        answer = 'Game: {0}\nId: {1}\nGame date: {2}\nGame time: {3}\n\r'.format(game['name'].replace('/', ' / '),
                                                                                 game['id'],
                                                                                 datetime[0],
                                                                                 datetime[1][:-1])

        bot.send_message(message.chat.id, answer)


def choice_keyboard():
    user_markup = types.ReplyKeyboardMarkup(True)
    user_markup.row("Return last games")
    user_markup.row("Exit")

    return user_markup


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     "Hello, {}!\nWelcome to the LastGamesBot!\n ".format(message.from_user.first_name),
                     reply_markup=choice_keyboard())


@bot.message_handler(func=lambda message: message.text == "Exit", content_types='text')
def exiting(message):
    bot.send_message(message.chat.id, "Goodbye!", reply_markup=types.ReplyKeyboardRemove())


if __name__ == "__main__":
    bot.polling()
