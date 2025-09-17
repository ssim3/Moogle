import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.users import start
from handlers.notes import get_note_handler
from handlers.folders import get_folder_handler

from dotenv import load_dotenv
import os

load_dotenv()
BOT_API_KEY = os.getenv("BOT_API_KEY")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":

    application = ApplicationBuilder().token(BOT_API_KEY).build()

    # --- Handlers Setup ---
    start_handler = CommandHandler("start", start)
    note_create_handler = get_note_handler()
    folder_create_handler = get_folder_handler()

    # --- Add Handlers ---
    application.add_handler(start_handler)
    application.add_handler(note_create_handler)
    application.add_handler(folder_create_handler)

    application.run_polling()
