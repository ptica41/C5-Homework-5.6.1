import telebot
from config import TOKEN, keys
from extensions import ConvertException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def hello(message):
    text = """Для конвертации валюты пришли мне сообщение:
<валюта, которая есть> <валюта, которая нужна> <количество, которое есть>
Валюты указывать через пробел в именительном падеже и со строчной буквы
Пример:
*доллар рубль 1*
Информация о доступных валютах /values"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['values'])
def hello(message):
    text = "Доступные валюты:\n"
    for _ in keys.keys():
        text += _ + '\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler()
def convert(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise ConvertException('Количество параметров должно быть 3!\nПомощь /help\nДоступные валюты /values')
        base, quote, amount = values
        count = Converter.get_price(base, quote, amount)
    except ConvertException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, f'Ошибка сервера!\n{e}')
    else:
        bot.reply_to(message, f'Цена {amount} {base} в {quote} = {"%.2f" % count}')


@bot.message_handler(content_types=['audio', 'voice', 'photo', 'video'])
def convert(message):
    bot.reply_to(message, 'Неверный формат!\nПомощь /help\nДоступные валюты /values')


bot.polling()
