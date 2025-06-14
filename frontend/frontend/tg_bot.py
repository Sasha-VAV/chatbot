import os
import time

import requests
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

TOKEN = os.environ.get("TG_BOT_TOKEN")
backend_url = "http://backend:8000"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    request = requests.post(
        backend_url + "/",
        json={"name": user_input, "age": time.localtime(time.time()).tm_sec},
    )
    await update.message.reply_text(f"Hello {request.json()['message']}")


if __name__ == "__main__":
    print("Bot is starting...")  # This will print
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running. Press Ctrl+C to stop.")  # This will print before blocking
    app.run_polling()  # This blocks execution (last line)
