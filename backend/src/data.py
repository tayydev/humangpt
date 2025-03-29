from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class QuestionStatus(BaseModel):
    uuid: str
    estimated_seconds: int

class Message(BaseModel):
    user_id: str
    name: str
    content: str
    is_answer: bool

class Session(BaseModel):
    user_id: str  # uuid
    title: str
    created_at: str = datetime.now().strftime("%Y-%m-%d")
    created_timestamp: datetime = datetime.now()
    uuid: str
    content: list[Message] = []

class UserPublic(BaseModel):
    uuid: str
    display_name: str
    pfp_url: str

class UserSecret(BaseModel):
    uuid: str
    display_name: str
    pfp_url: str
    # todo: google secret

    def to_pub(self):
        return UserPublic(
            uuid=self.uuid,
            display_name=self.display_name,
            pfp_url=self.pfp_url
        )
