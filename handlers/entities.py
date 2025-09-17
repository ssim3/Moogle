from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from database.queries import get_entities

async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # cwd represents the ObjectID of the folder that the user is currently inside
    try:
        cwd = context.user_data["cwd"]
    except KeyError:
        cwd = None

    telegram_id = update.message.from_user.id
    entities, entities_count = get_entities(telegram_id, cwd)

    if entities_count == 0:
        await update.message.reply_text(
            f"No files in folder: {'root' if cwd is None else cwd}",
            parse_mode="Markdown",
        )
        return

    message = f"*📂 Directory:* `{'root' if cwd is None else cwd}`\n\n"

    for i, entity in enumerate(entities, start=1):
        icon = '📁' if entity['type'] == 'folder' else '📝'
        name = f"`{entity['name']}`" if entity['type'] == 'folder' else entity['name'] # This is so fucking dumb but I need to use `` to have code highlighting to differentiate folders and notes
        message += f"\t{i}. {icon} {name}\n"

    message += "\n_Select a number to open a folder or view a note._"

    await update.message.reply_text(
        message,
        parse_mode="Markdown",
    )
