from flask import Flask, request
import os
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from mainbot import *



bot = Bot('6557277705:AAHWeNRzvuaicVr0Kumwa0CM8wQ4Q2-woCU')

app = Flask(__name__)

@app.route('/webhook', methods=["POST", "GET"])
def hello():
    if request.method == 'GET':
        return 'hi from Python2022I'
    elif request.method == "POST":
        data = request.get_json(force = True)

        dispacher: Dispatcher = Dispatcher(bot, None, workers=0)
        update:Update = Update.de_json(data, bot)

        dispacher.add_handler(CommandHandler('start',start))

    # ConversationHandlerni qo'shish
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('adding',save_info)],
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
        dispacher.add_handler(conv_handler)
        dispacher.add_handler(MessageHandler(Filters.text('Statistikam🗒'),my_statistik))
        dispacher.add_handler(CallbackQueryHandler(AdminSetting,pattern='admin'))
        dispacher.add_handler(CallbackQueryHandler(statistika,pattern='stc'))
        dispacher.add_handler(MessageHandler(Filters.regex(r'^\+'),addadmin))
        dispacher.add_handler(MessageHandler(Filters.regex(r'^\-'),deladmin))
        #update



        dispacher.process_update(update)
        return 'ok'

if __name__=='__main__':
    app.run()