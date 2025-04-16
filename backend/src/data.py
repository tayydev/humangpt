from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel

class QuestionStatus(BaseModel):
    uuid: str
    estimated_seconds: int

class Message(BaseModel):
    user_id: str
    name: str
    pfp_url: str
    content: str
    is_answer: bool

class Session(BaseModel):
    user_id: str  # uuid
    title: str
    created_at: str = datetime.now().strftime("%Y-%m-%d")
    updated_timestamp: datetime = datetime.now(timezone.utc)
    uuid: str
    content: list[Message] = []

    def to_dto(self):
        return SessionDTO(
            uuid=self.uuid,
            user_id=self.user_id,
            title=self.title,
            created_at=self.created_at,
            updated_timestamp=self.updated_timestamp
        )

class SessionDTO(BaseModel):
    uuid: str
    user_id: str  # uuid
    title: str
    created_at: str = datetime.now().strftime("%Y-%m-%d")
    updated_timestamp: datetime = datetime.now()

class UserPublic(BaseModel):
    uuid: str
    display_name: str
    pfp_url: str

class UserSecret(BaseModel):
    uuid: str
    display_name: str
    pfp_url: str
    ip: str
    # todo: google secret

    # returns everything that isn't secret about this person
    def to_pub(self):
        return UserPublic(
            uuid=self.uuid,
            display_name=self.display_name,
            pfp_url=self.pfp_url
        )
