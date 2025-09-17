from telegram import Update
from telegram.ext import ContextTypes

from database.models import User
from database.queries import create_user

from utils.messages import start_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    username = update.effective_user.username
    telegram_id = update.effective_user.id

    user = User(username=username, telegram_id=telegram_id)
    create_user(user)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_message(username),
        parse_mode="MarkdownV2",
    )
