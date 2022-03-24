# Практическое задание - проект "Telegram-бот для конвертации валюты".
# Имя: @My_MoneyConverter_Bot
# Выполнил: студент группы FPW-60 Ильин Максим.
# Дата: 24.03.2022

import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Для начала работы введите команду боту в следующем формате через пробел:\n\n " \
           "<валюта> \ <валюта конвертации> \ <количество>\n\nСписок доступных валют доступен по команде: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException("Неверное число параметров. Ввод в следующем формате через пробел: <валюта> \
<валюта конвертации> \
<количество>")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Стоимость {amount} {quote} в {base} это {total_base}"
        bot.send_message(message.chat.id, text)

bot.polling()