import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Получаем токен из переменных окружения
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://finance-bot-hi95.onrender.com{WEBHOOK_PATH}"  # ← замени на свой URL, если другой

# Flask-приложение
app = Flask(__name__)

# Создаём Telegram-приложение
application = Application.builder().token(TOKEN).build()

# Хендлер /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает! 🚀")

# Регистрируем хендлер
application.add_handler(CommandHandler("start", start))

# Flask Webhook
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)  # используем бот из Application
    await application.process_update(update)
    return "OK"

# Запуск
if __name__ == "__main__":
    async def run():
        await application.initialize()
        await application.start()
        print("Бот запущен ✅")

    loop = asyncio.get_event_loop()
    loop.create_task(run())
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
