import telebot
from config import tokenTg
from config import currs
from extensions import BrokerAPI

bot = telebot.TeleBot(tokenTg)

currs_list = [el for el in currs.keys()]


@bot.message_handler(commands=['start', 'help'])
def send_welcome_help(message):
    # print(message.json)
    add = ''
    if message.text.find('/start') > -1:
        add = f"Welcome, {message.from_user.first_name}! \n"

    bot.send_message(message.chat.id, add +
                     "You can make request for exchange rate of this " +
                     "currencies: (" + ', '.join(currs_list) + ') \n' +
                     "Request format: <curr1> <curr2> <amount> \n" +
                     "Example: доллар рубль 11.5"
                     )


@bot.message_handler(commands=['values'])
def send_values_list(message):
    bot.send_message(message.chat.id, f"Available currencies: (" + ', '.join(currs_list) + ')')


@bot.message_handler(content_types=['text'])
def general_handler(message):
    try:
        base, quote, amount = BrokerAPI.check_input(message.text)
        base = BrokerAPI.get_synonym(base)
        quote = BrokerAPI.get_synonym(quote)
        rate = BrokerAPI.get_price(base, quote, amount)

    except Exception as err:
        bot.send_message(message.chat.id, f'Error occurs: {err}')

    else:
        answer = f'{amount} {base} = {rate} {quote}'
        bot.reply_to(message, answer)


bot.infinity_polling()
