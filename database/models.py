from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field
from bson import ObjectId

# --- User Schema ---
class User(BaseModel):
    telegram_id: int
    username: str

# --- Notes and Folders Schema --- 
class Entity(BaseModel):
    telegram_id: int                 # owner of the note/folder
    type: Literal["note", "folder"]  # whether it's a note or folder
    name: str 
    content: Optional[str] = None    # used if it's a note
    parent_id: Optional[ObjectId] = None  # null = root folder
    created_at: datetime = Field(default_factory=datetime.utcnow())
 