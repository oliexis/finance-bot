import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация Flask-сервера
app = Flask(__name__)

# Функция команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает! 🚀")

# Инициализация Telegram-приложения
application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Фоновый запуск Telegram-бота
import threading
def run_telegram():
    application.run_polling()

threading.Thread(target=run_telegram).start()

# Запускаем Flask-сервер
@app.route("/")
def index():
    return "Бот активен на Render 🎯"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
