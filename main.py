import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL = f"https://finance-bot-hi95.onrender.com{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает! 🚀")

application.add_handler(CommandHandler("start", start))

# Вебхук обработчик
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    await application.initialize()
    await application.process_update(update)
    return "OK"

if __name__ == "__main__":
    async def run():
        await application.initialize()
        await application.start()
        print("Bot initialized and started.")

    loop = asyncio.get_event_loop()
    loop.create_task(run())

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
