import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    asyncio.run_coroutine_threadsafe(application.process_update(update), application.bot.loop)
    return "OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает! 🚀")

application.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    import threading

    def run_app():
        app.run(host="0.0.0.0", port=10000)

    threading.Thread(target=run_app).start()
    asyncio.run(application.run_polling())
