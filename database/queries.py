from .connection import db
from .models import User
import pymongo

users = db["users"]
users.create_index("telegram_id", unique=True)

def create_user(user: User):
    try:
        return users.insert_one(user.model_dump())
    except pymongo.errors.DuplicateKeyError:
        pass 
