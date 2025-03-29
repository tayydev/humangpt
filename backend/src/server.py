from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from service import *
from data import *
from service import get_or_create
import random

app = FastAPI()

# Configure CORS middleware with broad settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    # Allow credentials (cookies, authorization headers)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/submit")
async def submit(msg: str, user_id: str, is_answer: bool, uuid: Optional[str] = None) -> Session:
    session = get_or_create(uuid, title=msg)
    user = get_user_info(user_id)
    session.content.append(Message(name=user.display_name, pfp_url=user.pfp_url, content=msg, is_answer=is_answer))  # append new content
    return write_session(session)


@app.get("/session/{uuid}")
async def get_session(uuid: str):
    return get_only(uuid)


@app.get("/unanswered_sessions")
async def get_unanswered(answerer_id: str) -> list[Session]:
    sessions = get_sessions()
    unanswered = []
    for session in sessions:
        if not session.content[-1].is_answer and not session.user_id == answerer_id:
            unanswered.append(session)
    unanswered = sorted(unanswered, key=lambda s: s.created_timestamp)
    unanswered = unanswered[:3]
    random.shuffle(unanswered)
    return unanswered

@app.post("/guest_user")
async def guest() -> UserPublic:
    return create_temp_user()
