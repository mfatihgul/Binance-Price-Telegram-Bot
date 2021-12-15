import logging

import telegram
from telegram import update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests, json

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger(__name__)

class Tracker:
    def __init__(self):
        self.TOKEN = "" #Telegram Bot Token (BotFather)
        self.bot = telegram.Bot(self.TOKEN)
    
    def p(self, update, context):
        chat_id = update.effective_chat.id
        try:
            command, coinname = (update.message.text).split(" ")
        except ValueError:
            self.reply_user(chat_id=chat_id, text="Wrong format.")
            return 0
        coinname = coinname.upper()
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coinname}USDT")
        coinusdt = json.loads(response.content)

        if 'msg' in coinusdt:
            self.reply_user(chat_id=chat_id, text="There's no coin named {coinname} in Binance.")
            return 0
        else:
            usdt_text = f"{float(coinusdt['price']):.4f}"

            text = coinname + " " + usdt_text #You can edit this variable to change what to send to the Telegram bot
            self.reply_user(chat_id=chat_id, text=text)
    def reply_user(self, chat_id, text):
        error_count = 0
        while True:
            try:
                self.bot.send_message(chat_id=chat_id, text=text)
                break
            except Unauthorized:
                print(f"send_message_to_telegram -> Unauthorized Error")
            except Exception as e:
                print(f"send_message_to_telegram ->Error as {e}")
                error_count += 1
                if error_count == 6:
                    break
                time.sleep(1)
    
    def main(self):
        updater = Updater(self.TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler('p', self.p))
        dp.add_handler(CommandHandler('price', self.p))

        updater.start_polling()
        updater.idle()

b = Tracker()
b.main()
