from pydantic import BaseModel

class QuestionStatus(BaseModel):
    uuid: str
    estimated_seconds: int

class Message(BaseModel):
    name: str
    content: str
    is_answer: bool

class Session(BaseModel):
    uuid: str
    content: list[Message] = []
