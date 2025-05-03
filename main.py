from flask import Flask
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    from flask import request
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return "OK"

def start(update, context):
    update.message.reply_text("Бот работает! 🚀")

dp = Dispatcher(bot, None, workers=0)
dp.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
