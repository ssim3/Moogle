import telegramify_markdown
from telegramify_markdown import customize

def start_message(username: str):
    message = rf"""
Welcome to **TeleNotes** @{username}! 👋

Send me your notes in the following format and I will save them for you:
>/note [note title] [note content]

For example:
>/note Meeting Discuss project roadmap with team

To organize your notes into folders, add a path like this:
>/note Work/Meetings Meeting Discuss project roadmap

📁 View all notes: 
>/list

📁 View notes in a folder: 
>/list [folder path]

🗑️ Delete your last note:
>/delete [note path]

📁 Create a folder: 
>/folder

The full list of commands is available by sending /help
"""
    
    message_mv2 = telegramify_markdown.markdownify(
        message
    )

    return message_mv2
