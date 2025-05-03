import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. Получаем токен
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

# 2. Flask сервер
app = Flask(__name__)

# 3. Telegram bot приложение
application = Application.builder().token(TOKEN).build()

# 4. Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает! 🚀")

application.add_handler(CommandHandler("start", start))

# 5. Webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return "OK"

# 6. Запуск сервера
def run():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run).start()
