import os
import asyncio
import threading
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает! 🚀")

application.add_handler(CommandHandler("start", start))

def run_app():
    app.run(host="0.0.0.0", port=10000)

async def start_application():
    await application.initialize()
    await application.start()
    await application.updater.start_polling()  # нужно для готовности очереди

if __name__ == "__main__":
    threading.Thread(target=run_app).start()
    asyncio.run(start_application())
