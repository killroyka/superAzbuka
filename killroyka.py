import logging
import telegram
import config
import datetime as dt
import models
import math
from random import choice

work = ["moyka today", "иди мой", "недомойка", "мой чисто)))", "опять работа"]
mama = ["MOM", "мама", '"рабыня из ора"']
zuf = ["ZufikPufik", "Зуфар", "Пуфик", "Мелкий", "Зуфика"]
tag = ['Такир', "KILLROYKA", "Доченька", "Прынц", "Приемный)))"]
a = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'p', 'a', 's', 'd', 'f',
     'g', 'h', 'j', 'k', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '2',
     '3', '4', '5', '6', '7', '8', '9',
     'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'P', 'A', 'S', 'D', 'F',
     'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
c = 0

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/blala, /kaka, /start, /last kol vo ras, /pass kol vo ras, /resh a b c')


b = []


def generate_password(update, context: CallbackContext):
    for x in range(int(context.args[0])):
        b.append(choice(a))
    c = ''.join(b)
    b.clear()
    update.message.reply_text(c)


def Who_is_moyka_today(update, context):
    a = choice(work)
    if dt.date.today().day % 2 == 0 and dt.date.today().day != 31:
        if a != "опять работа":
            update.message.reply_text(choice(zuf))
            update.message.reply_text(a)
        else:
            update.message.reply_text(a)
    elif dt.date.today().day % 2 != 0 and dt.date.today().day != 31:
        if a != "опять работа":
            update.message.reply_text(choice(tag))
            update.message.reply_text(a)
        else:
            update.message.reply_text(a)
    else:
        if a != "опять работа, бля":
            update.message.reply_text(choice(mama))
            update.message.reply_text(a)
        else:
            update.message.reply_text(a)


def roots_of_quadratic_equation(update, context: CallbackContext):
    alpha = int(context.args[0])
    beta = int(context.args[1])
    charlie = int(context.args[2])
    result = []
    if alpha == 0 and beta == 0 and charlie == 0:
        result.append('all')
    elif alpha != 0:
        d = (beta * beta) - (4 * alpha * charlie)
        if d > 0:
            x1 = (beta * -1 + math.sqrt(d)) / (2 * alpha)
            x2 = (beta * -1 - math.sqrt(d)) / (2 * alpha)
            result.append(int(x1))
            result.append(int(x2))
        elif alpha == 0 and beta == 0 and charlie == 0:
            result.append('all')
        elif d == 0:
            x1 = (beta * -1 + math.sqrt(d)) / (2 * alpha)
            result.append(x1)
    elif beta != 0 and charlie != 0:
        result.append(-charlie / beta)
    print(result)
    for x in result:
        update.message.reply_text(x)


def update(update, context):
    update.massege.reply_text('i am alive')


def geom(update, context: CallbackContext):
    b = int(context.args[0])
    q = int(context.args[1])
    n = int(context.args[2])
    update.message.reply_text(b * q ** (n - 1))


def blala(update, context: CallbackContext):
    c = int(context.args[0])
    for x in range(c + 1):
        update.message.reply_text(x)
    c += 1
    update.message.reply_text('ya sdelal')


def kaka(update, context):
    global c
    c = 0
    update.message.reply_text('teper c = 0')


def save(update, context):
    msg: telegram.Message = update.message

    models.User.get_or_create(
        tg_id=msg.from_user.id,
        defaults={
            'full_name': msg.from_user.full_name
        }
    )

    models.Message.create(
        message_id=msg.message_id,
        chat_id=msg.chat_id,
        text=msg.text,
        tg_id=msg.from_user.id
    )


def last(update, context: CallbackContext):
    last_message = 10
    if len(context.args) > 0:
        last_message = int(context.args[0])
    msg: telegram.Message = update.Message
    for msg2 in models.Message.filter(chat_id=msg.chat_id).order_by(models.Message.id.desc()).limit(last_message):
        update.message.reply_text(msg2.text)


def echo3(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("blala", blala))
    dp.add_handler(CommandHandler("last", last))
    dp.add_handler(CommandHandler("pass", generate_password))
    dp.add_handler(CommandHandler("resh", roots_of_quadratic_equation))
    dp.add_handler(CommandHandler("geom", geom))
    dp.add_handler(CommandHandler("ktomoyka", Who_is_moyka_today))
    dp.add_handler(MessageHandler(Filters.text, echo3))

    if config.HEROKU_APP_NAME is None:
        updater.start_polling()
    else:
        updater.start_webhook(listen='0.0.0.0',
                              port=config.PORT,
                              url_path=config.TOKEN)
        updater.bot.set_webhook(f"https://{config.HEROKU_APP_NAME}.herokuapp.com/{config.TOKEN}")
save()
if __name__ == '__main__':
    main()
