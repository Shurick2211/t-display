import socket
from time import sleep

from crypto_price import get_crypto_price
from utelegram import Bot

TOKEN = "2095334227:AAG8OW8-6J0oNib9J21OHLWePnyx8T85CoE"

def start_bot():
  bot = Bot(token=TOKEN)
  bot.start_loop()

  @bot.add_command_handler('crypto')
  def handle_bitcoin(update):
    price = get_crypto_price()
    btc = f"Btc: {price["bitcoin"]["usd"]}$"
    eth = f"Eth: {price["ethereum"]["usd"]}$"
    xpr = f"Xpr: {price["ripple"]["usd"]}$"
    text = f"{btc}\n{eth}\n{xpr}"
    update.reply(text)
    print(text)

  @bot.add_command_handler('help')
  def handle_help(update):
    update.reply("Помоги себе сам командами:\n/crypto\n/led\n/help")
    print("Команда /help вызвана.")

  @bot.add_command_handler('led')
  def handle_help(update):
    update.reply("Мигает!!!")

  @bot.add_command_handler('start')
  def handle_start(update):
    print("Команда старт")
    id = update.message['chat']['id']
    name = update.message['from']['first_name']
    bot.send_message(id, f"Привет, {name}!\nНачни с /help")
    print(update.message['from'])

  @bot.add_message_handler(r'.*')
  def handle_message(update):
    user = update.message['from']['id']
    text = update.message['text']
    update.reply(f"{user}! I don`t know: {text}")
    print(f'USER - {user} SAYS: {text}')