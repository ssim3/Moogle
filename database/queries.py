from .connection import db
from .models import User
import pymongo

users = db["users"]
users.create_index("telegram_id", unique=True)

entities = db["entities"]

# --- User Queries --- 
def create_user(user: User):
    try:
        return users.insert_one(user.model_dump())
    except pymongo.errors.DuplicateKeyError:
        pass 

# --- Folders Queries ---
#def create_folder(folder: Entity):
#    return entities.insert_one(folder.model_dump())

# --- Notes Queries ---
#def create_note(note: Entity):
#    return entities.insert_one(note.model_dump())

