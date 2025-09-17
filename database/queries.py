from .connection import db
from .models import User, Entity
import pymongo
from typing import Union
from bson import ObjectId

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
def create_folder(telegram_id: int, name: str, parent_id: str) -> bool:

    folder = Entity(
        telegram_id=telegram_id, type="folder", name=name, parent_id=parent_id
    )

    return entities.insert_one(folder.model_dump())


# --- Notes Queries ---
def create_note(telegram_id: int, title: str, content: str, parent_id: str) -> bool:

    note = Entity(
        telegram_id=telegram_id,
        type="note",
        name=title,
        content=content,
        parent_id=parent_id,
    )

    return entities.insert_one(note.model_dump())


# --- Validation Queries ---
def validate_path(user_id: str, path: str) -> Union[None, ObjectId, bool]:

    if path == "/":
        return None

    # Get full folder directory
    parts = [p for p in path.strip("/").split("/")]

    parent_id = None

    for part in parts:

        folder = entities.find_one(
            {
                "telegram_id": user_id,
                "name": part,
                "type": "folder",
                "parent_id": parent_id,
            }
        )

        if not folder:
            return False  # invalid path

        # Set ID of parent folder to parent_id of entity we are creating
        parent_id = folder["_id"]

    return parent_id  # returns the folder id where the note should be created
