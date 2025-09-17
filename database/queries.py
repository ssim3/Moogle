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


# --- Entity Queries ---
def get_entities(telegram_id: int, parent_id: str):
    
    """ Returns all the entities in specified folder parent_id """

    filter = {
        "telegram_id": telegram_id,
        "parent_id": parent_id,
    }

    results_count = entities.count_documents(filter)
    results = entities.find(filter)

    if not results:
        return False
    
    return results, results_count


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
def validate_path(telegram_id: int, path: str) -> Union[None, ObjectId, bool]:
    """
    Validates whether the path a user enters exists.
    Returns the parent folder's ObjectId, None for root folder, and False if it doesn't exist.
    """

    if path == "/":
        return None

    # Get full folder directory
    parts = [p for p in path.strip("/").split("/")]

    parent_id = None

    for part in parts:

        folder = entities.find_one(
            {
                "telegram_id": telegram_id,
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


def check_duplicate_entity(
    telegram_id: int, parent_id: ObjectId, file_name: str, type: str
):

    entity = entities.find_one(
        {
            "telegram_id": telegram_id,
            "name": file_name,
            "parent_id": parent_id,
            "type": type,
        }
    )

    if entity:
        return False  # Exists a duplicate

    return True
