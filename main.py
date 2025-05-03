from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import os

TOKEN = os.environ.get("BOT_TOKEN")  # ← безопасно и гибко
bot = Bot(token=TOKEN)
app = Flask(__name__)

application = Application.builder().token(TOKEN).build()


@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "OK"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает! 🚀")


application.add_handler(CommandHandler("start", start))


async def main():
    await application.initialize()
    await application.start()
    # Здесь не вызываем application.updater.start_polling(), потому что мы используем webhook
    await application.updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path=TOKEN,
        webhook_url=f"https://finance-bot-hi95.onrender.com/{TOKEN}",
    )
    await application.updater.idle()


if __name__ == "__main__":
    asyncio.run(main())
