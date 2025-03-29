import random
from typing import Optional
from uuid import uuid4

from data import *

session_store: dict[str, Session] = {}
user_store: dict[str, UserSecret] = {}

def get_only(uuid: str):
    return session_store[uuid]

def get_sessions():
    sessions = []
    for session in session_store.values():
        sessions.append(session)
    return sessions

def get_or_create(uuid: Optional[str], title: str, user_id: str):
    if uuid:
        return session_store[uuid]
    else:
        return Session(uuid=str(uuid4()), title=title, user_id=user_id)

def write_session(session: Session):
    session_store[session.uuid] = session
    return session

def create_temp_user() -> UserPublic:
    guest_id = str(uuid4())
    user_store[guest_id] = UserSecret(
        uuid=guest_id,
        display_name = "guest_user_" + str(random.randint(10000000, 99999999)),
        pfp_url="todo",
    )
    return user_store[guest_id].to_pub()

def get_user_info(uuid: str) -> UserPublic:
    return user_store[uuid].to_pub()
