from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler
from telegram import (
    Bot,Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,
    InlineKeyboardButton,ChatAdministratorRights,ParseMode
    )
import sqlite3

cnt = sqlite3.connect('data.db')
cr = cnt.cursor()

bot = Bot('6557277705:AAGnGBYgqwWnSNDarXDXwj__Eml6EcIobmQ')

def start(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot 
    chat_id = update.message.chat_id
    print(chat_id)
    command = f"""
        SELECT * FROM Admins WHERE user_id = "{chat_id}"
    """
    a=cr.execute(command).fetchall()
    print(a)
    if a:
        if a[0][3]==1:
            text = "Assalomu alaykum botga xush kelibsiz"
            btns = ReplyKeyboardMarkup([['Statistika','Admin⚙️']],resize_keyboard=True)
            bot.sendMessage(chat_id,text,reply_markup=btns)
        else:
            text = "Assalomu alaykum botga xush kelibsiz"
            btns = ReplyKeyboardMarkup([['Statistika','Ma\'lumot qo\'shish']],resize_keyboard=True)
            bot.sendMessage(chat_id,text,reply_markup=btns)


def viloyat(update:Update, context:CallbackContext):
    btns=[
        ['Тошкент ш','Тошкент в'],
        ['Андижон в.','Бухоро в.'],
        ['Жиззах в.','Қашқадарё в'],
        ['Навоий в.','Наманган в.'],
        ['Самарқанд в.','Сурхондарё в.'],
        ['Сирдарё в.','Фарғона в'],
        ['Хоразм в','Қорақалпоқ р']
    ]
    btn=ReplyKeyboardMarkup(btns)
    bot=context.bot 
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id,text='Tanlang',reply_markup=btn)


updater=Updater('6557277705:AAGnGBYgqwWnSNDarXDXwj__Eml6EcIobmQ')

updater.dispatcher.add_handler(CommandHandler('start',start))

updater.start_polling()
updater.idle()