import telebot
import requests
import json
from telebot import types


URL = 'https://api.bitaps.com/market/v1/ticker/btcusd'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def parse():
    html = get_html(URL)
    bt = json.loads(html.text)
    return bt['data']['last']


# parse()

bot = telebot.TeleBot('5597472270:AAHkFEBR3MlKuXel83R07kzvbMGoX0sOPx4')


@bot.message_handler(commands=['btc'])
def btc(message):
    bot.send_message(message.chat.id, parse())


#@bot.message_handler(commands=['btcc'])
def button_btc(price):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('BTC', '1'))
    bot.send_message(price.chat.id, ' price BTC', reply_markup=markup)


bot.polling(none_stop=True)
