import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return "OK"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает! 🚀")

application.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    import asyncio
    async def run():
        await application.initialize()
        await application.start()
        print("Bot is ready and webhook is set.")

    asyncio.run(run())
    app.run(host="0.0.0.0", port=10000)
