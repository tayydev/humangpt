import random
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException

from settings import *
from data import *

def get_sessions_collection():
    return get_mongodb_connection()["sessions"]

def get_sessions_list():
    raw_sessions = list(get_sessions_collection().find())
    return [Session.model_validate(session) for session in raw_sessions]

def get_session(uuid : str) -> Session:
    collection = get_sessions_collection()
    session = collection.find_one({"_id" : uuid})
    return Session.model_validate(session) if session else None

# creates pydantic Session type
def get_or_create_session(uuid: Optional[str], title: str, user_id: str):
    if uuid:
        return get_session(uuid)
    else:
        return Session(uuid=str(uuid4()), title=title, user_id=user_id)

# puts Session into database
def write_session(session: Session):
    session_data = session.model_dump()
    get_sessions_collection().update_one(
        {"_id" : session.uuid},
        {"$set" : session_data},
        upsert=True  # updates session if it exists
    )
    return session

def get_users_collection():
    return get_mongodb_connection()["users"]

def create_temp_user() -> UserPublic:
    guest_id = str(uuid4())
    user = UserSecret(
        uuid=guest_id,
        display_name = "guest_user_" + str(random.randint(10000000, 99999999)),
        pfp_url="guest_url",
    )
    user_data = user.model_dump()
    get_users_collection().update_one(
        {"_id" : guest_id},
        {"$set" : user_data},
        upsert=True
    )
    return user.to_pub()

def get_user_info(uuid: str) -> UserPublic:
    try:
        collection = get_users_collection()
        user = collection.find_one({"_id" : uuid})
        return UserSecret.model_validate(user).to_pub()
    except KeyError:
        raise HTTPException(status_code=404, detail=f"User with ID '{uuid}' not found")
