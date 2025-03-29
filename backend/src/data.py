from datetime import datetime

from pydantic import BaseModel

class QuestionStatus(BaseModel):
    uuid: str
    estimated_seconds: int

class Message(BaseModel):
    name: str
    content: str
    is_answer: bool

class Session(BaseModel):
    title: str = "My First Chat"
    created_at: str = datetime.now().strftime("%Y-%m-%d")
    uuid: str
    content: list[Message] = []
    is_reserved: bool = False
