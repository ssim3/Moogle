from database.models import Entity
from database.queries import validate_path, create_note
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

CONTENT, PATH = range(2)


async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry Point for /note command"""

    # If user doesn't provide a title
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /note [title]")
        return ConversationHandler.END

    context.user_data["title"] = " ".join(context.args)
    await update.message.reply_text(
        f"New Note: *{context.user_data['title']}*\n\n📝 Please send me the contents of your note.\n\n❌ Use /cancel to cancel note creation.",
        parse_mode="Markdown",
    )

    return CONTENT


async def content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get content of current note"""

    context.user_data["content"] = update.message.text

    await update.message.reply_text(
        "Great! Now, where should I save this note?\n\nSend a path to a folder (e.g. `Hobbies/MartialArts`) (default: `/`).",
        parse_mode="Markdown",
    )

    return PATH


async def path(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Capture path and save note"""

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

    result = create_note(
        telegram_id=telegram_id,
        title=context.user_data["title"],
        content=context.user_data["content"],
        parent_id=parent_id,
    )

    if result:
        await update.message.reply_text(
            f"✅ New Note Created!\n\n*Title:* {context.user_data['title']}\n*Path:* `{path}`\n\n{context.user_data['content']}",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(f"❌ Note creation failed. Please try again.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel note creation"""

    await update.message.reply_text("❌ Note creation cancelled.")
    return ConversationHandler.END


def get_note_handler():
    """Return the conversation handler for notes"""

    return ConversationHandler(
        entry_points=[CommandHandler("note", note)],
        states={
            CONTENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, content)],
            PATH: [MessageHandler(filters.TEXT & ~filters.COMMAND, path)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
