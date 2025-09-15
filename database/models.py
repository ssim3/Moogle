from pydantic import BaseModel, Field
from datetime import datetime

# --- User Schema ---
class User(BaseModel):
    telegram_id: int
    username: str

class Note(BaseModel):
    telegram_id: int
    title: str
    content: str
    path: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
