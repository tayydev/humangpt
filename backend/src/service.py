from typing import Optional
from uuid import uuid4

from data import *

storage: dict[str, Session] = {}

def get_only(uuid: str):
    return storage[uuid]

def get_sessions():
    sessions = []
    for session in storage.values():
        sessions.append(session)
    return sessions

def get_or_create(uuid: Optional[str]):
    if uuid:
        return storage[uuid]
    else:
        return Session(uuid=str(uuid4()))

def write_session(session: Session):
    storage[session.uuid] = session
    return session
