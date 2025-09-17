from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from database.queries import create_folder, validate_path, check_duplicate_entity

PATH = range(1)


async def folder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text("Usage: /folder [name]")
        return ConversationHandler.END

    context.user_data["folder_name"] = " ".join(context.args)

    await update.message.reply_text(
        f"New 📁: *{context.user_data['folder_name']}*\n\n📝 Now, where should I save this folder?\n\nSend a path to a folder (e.g. `Hobbies/MartialArts`) (default: `/`).\n\n❌ Use /cancel to cancel folder creation.",
        parse_mode="Markdown",
    )

    return PATH


async def path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Capture path and save folder"""

    folder_name = context.user_data["folder_name"]
    telegram_id = update.effective_user.id
    path = update.message.text.strip()

    # Validate the path that user enters.
    # - Returns None if root path is specified
    # - Returns the ObjectID of the folder the note will belong to
    # - Returns FALSE if the path does not exists
    parent_id = validate_path(update.effective_user.id, path)

    if parent_id is False:
        await update.message.reply_text("⚠️ Path does not exist! Please try again.")
        return PATH

    # Validates whether folder already exists or not
    if (
        check_duplicate_entity(telegram_id, parent_id, folder_name, type="folder")
        is False
    ):
        await update.message.reply_text(
            f"⚠️ Folder **{folder_name}** already exists in **{path}**!\n\nPlease enter another Path.",
            parse_mode="Markdown",
        )
        return PATH

    result = create_folder(
        telegram_id=telegram_id,
        name=folder_name,
        parent_id=parent_id,
    )

    if result:
        await update.message.reply_text(
            f"✅ New Folder Created!\n\n📁 {folder_name}\n*Path:* `{path}`",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(f"❌ Folder creation failed. Please try again.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel note creation"""

    await update.message.reply_text("❌ Folder creation cancelled.")
    return ConversationHandler.END


def get_folder_handler():
    """Return the conversation handler for notes"""

    return ConversationHandler(
        entry_points=[CommandHandler("folder", folder)],
        states={
            PATH: [MessageHandler(filters.TEXT & ~filters.COMMAND, path)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
