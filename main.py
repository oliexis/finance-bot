from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import os

TOKEN = os.environ.get("BOT_TOKEN")  # переменная окружения
bot = Bot(token=TOKEN)
app = Flask(__name__)
application = Application.builder().token(TOKEN).build()


@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return "ok"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот успешно запущен!")


application.add_handler(CommandHandler("start", start))


def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run():
        await application.initialize()
        await application.start()
        print("Bot initialized and running...")

    loop.run_until_complete(run())


if __name__ == "__main__":
    # Запускаем телеграм-бота в фоне
    import threading
    threading.Thread(target=start_bot).start()

    # Запускаем Flask — Render увидит открытый порт
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
