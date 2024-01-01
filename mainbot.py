from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler,ConversationHandler
from telegram import (
    Bot,Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,
    InlineKeyboardButton,ChatAdministratorRights,ParseMode, MenuButtonWebApp,WebAppInfo
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
    command = f"""
        SELECT * FROM Admins WHERE user_id = "{chat_id}"
    """
    a=cr.execute(command).fetchall()
    if a:
        if a[0][2]=='1':
            text = "Assalomu alaykum botga xush kelibsiz, bo'limlardan birini tanlang."
            btn1 = InlineKeyboardButton('Statistika',callback_data=f'stc')
            btn2 = InlineKeyboardButton('Admin⚙️',callback_data='admin stng')
            btn = InlineKeyboardMarkup([[btn1,btn2]])
        else:
            text = "Assalomu alaykum botga xush kelibsiz, bo'limlardan birini tanlang."
            btn1 = InlineKeyboardButton('Statistikam',callback_data=f'stc {chat_id}')
            btn2 = InlineKeyboardButton('Ma\'lumot qo\'shish',callback_data=f'add {chat_id}')
            btn = InlineKeyboardMarkup([[btn1,btn2]])
        bot.sendMessage(chat_id,text,reply_markup=btn)


def AdminSetting(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    bot.delete_message(chat_id,msg)
    d,b = query.data.split(' ')
    if b == 'stng':
        btn1 = InlineKeyboardButton('Admin qo\'shish', callback_data='admin +')
        btn2 = InlineKeyboardButton('Admin o\'chirish', callback_data='admin -')
        btn3 = InlineKeyboardButton('Adminlar', callback_data='admin lar')
        btn = InlineKeyboardMarkup([[btn1,btn2], [btn3]])
        bot.send_message(chat_id,'Bo\'limlardan birini tanlang',reply_markup=btn)
    elif b == '+':
        text = "Yangi admin qo'shish uchun qo'shmoqchi bo'lgan admininggizning telegram id sini\n+user_id - lavozimi\n holatda yozing"
        bot.send_message(chat_id,text)
    elif b == 'lar':
        cnt = sqlite3.connect('data.db')
        cr = cnt.cursor()
        command = """
        SELECT * FROM Admins
        """
        a = cr.execute(command).fetchall()
        k=1
        text = f"Adminlar👤\n\n"
        for i in a:
            text+=f"{k}) `{i[1]}` - {i[2]}"
        bot.sendMessage(chat_id,text,parse_mode=ParseMode.MARKDOWN)
    elif b == '-':
        text = "Adminni o'chirish uchun o'chirmoqchi bo'lgan admininggizning telegram id sini\n-user_id\n holatda yozing"
        bot.send_message(chat_id,text)


def addadmin(update:Update, context:CallbackContext):
    bot=context.bot 
    chat_id = update.message.chat_id
    data = update.message.text
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    command = f"""
        SELECT * FROM Admins WHERE user_id = "{chat_id}"
    """
    admin = cr.execute(command).fetchall()
    if admin:
        a,b = data[1:].split('-')
        command = f"""
        INSERT INTO Admins (user_id,status) VALUES ("{a.replace(' ','')}","{b.removeprefix(' ')}")
        """
        cr.execute(command)
        cnt.commit()
        bot.sendMessage(chat_id,'✅')


    
def deladmin(update:Update, context:CallbackContext):
    bot=context.bot 
    chat_id = update.message.chat_id
    data = update.message.text
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    command = f"""
        SELECT * FROM Admins WHERE user_id = "{chat_id}"
    """
    admin = cr.execute(command).fetchall()
    if admin:
        try:
            data = data[1:]
            cr.execute(f'DELETE FROM Admins WHERE user_id = "{data}"')
            cnt.commit()
            bot.sendMessage(chat_id,'☑️')
        except:
            bot.sendMessage(chat_id,'Qandaydir xatolik')


FIRST_NAME, FIRMA, PHONE_NUMBER, VIL, TUM, F_TUR, M_TUR = range(7)

def first(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    bot.delete_message(chat_id,msg)
    bot.sendMessage(chat_id,"Assalomu alaykum! Xaridor ismini kiriting.")
    return FIRST_NAME

def save_info(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['name'] = update.message.text
    update.message.reply_text("Firma nomini kiriting")
    return FIRMA

def firma(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['firma'] = update.message.text
    update.message.reply_text("Mijoz telefon raqamini kiriting:")
    return PHONE_NUMBER

def save_phone(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['phone_number'] = update.message.text
    btns=[
        ['Тошкент ш.','Тошкент в.'],
        ['Андижон в.','Бухоро в.'],
        ['Жиззах в.','Қашқадарё в'],
        ['Навоий в.','Наманган в.'],
        ['Самарқанд в.','Сурхондарё в.'],
        ['Сирдарё в.','Фарғона в.'],
        ['Хоразм в.','Қорақалпоғистон']
    ]
    btn=ReplyKeyboardMarkup(btns)
    update.message.reply_text("Viloyatni tanlang:",reply_markup=btn)
    return VIL


def select_tuman(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['viloyat'] = update.message.text
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    a = cr.execute(f'SELECT id FROM adress WHERE val02="{update.message.text}"').fetchone()
    try:
        b = cr.execute(f'SELECT name1 FROM adress WHERE int01={int(a[0])}').fetchall()
        btns = []
        for i in range(0, len(b), 2):
            if i + 1 < len(b):
                btns.append([b[i][0], b[i + 1][0]])
            else:
                btns.append([b[i][0]])
        btns = ReplyKeyboardMarkup(btns)
        update.message.reply_text("Tumanni tanlang:",reply_markup=btns)
        return TUM
    except:
        pass


def firma_turi(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['tuman'] = update.message.text
    btns = [
        ['Exportchi fabrika', 'Ichki bozor'],
        ['Kichik fabrika','Otele'],
        ['Yakkaxon chevar']
    ]
    btns = ReplyKeyboardMarkup(btns)
    update.message.reply_text("Faoliyat turini ko'rsating:",reply_markup=btns)
    return F_TUR
    
def m_turi(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['f_tur'] = update.message.text
    btns = [
        ['Exportchi fabrika', 'Ichki bozor'],
        ['Kichik fabrika','Otele'],
        ['Yakkaxon chevar']
    ]
    btns = ReplyKeyboardMarkup(btns)
    update.message.reply_text("Qiziqish bildirayotgan mahsulot turini ko'rsating:",reply_markup=btns)
    return M_TUR


def saving(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['m_tur'] = update.message.text

    # Ma'lumotlar to'landi
    context.bot.send_message(update.effective_chat.id, "Ma'lumotlar to'landi:\n"
                          f"Ism: {user_data['name']}\n"
                          f"Telefon raqam: {user_data['phone_number']}\n"
                          f"Firma nomi: {user_data['firma']}\n"
                          f"Manzil: {user_data['viloyat']} - {user_data['tuman']}\n"
                          f"Firma turi: {user_data['f_tur']}\n"
                          f"Mahsulot turi: {user_data['m_tur']}\n"
                          )
                          

    keyboard = [[InlineKeyboardButton("Ma'lumot to'ldirish", callback_data='info')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Assalomu alaykum! Malumotlarni to'ldirish uchun tugmani bosing.", reply_markup=reply_markup)
    
    # Ma'lumotlarni to'plangan o'ynani to'ldirish
    user_data.clear()

    return FIRST_NAME

def cancel(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data.clear()
    update.message.reply_text("Ma'lumot to'ldirish bekor qilindi.")
    return ConversationHandler.END




updater=Updater('6557277705:AAGnGBYgqwWnSNDarXDXwj__Eml6EcIobmQ')

updater.dispatcher.add_handler(CommandHandler('start',start))
dp = updater.dispatcher

    # ConversationHandlerni qo'shish
conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(first,pattern='add')],
    states={
        FIRST_NAME: [MessageHandler(Filters.text & ~Filters.command, save_info)],
        FIRMA: [MessageHandler(Filters.text & ~Filters.command, firma)],
        PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, save_phone)],
        VIL: [MessageHandler(Filters.text & ~Filters.command, select_tuman)],
        TUM: [MessageHandler(Filters.text & ~Filters.command,firma_turi)],
        F_TUR: [MessageHandler(Filters.text & ~Filters.command,m_turi)],
        M_TUR: [MessageHandler(Filters.text & ~Filters.command,saving)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
dp.add_handler(conv_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(AdminSetting,pattern='admin'))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'^\+'),addadmin))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'^\-'),deladmin))
updater.start_polling()
updater.idle()