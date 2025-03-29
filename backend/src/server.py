from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from service import *
from data import *
from service import get_or_create

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
async def submit(msg: str, source: str, is_answer: bool, uuid: Optional[str] = None) -> Session:
    session = get_or_create(uuid)
    session.content.append(Message(name=source, content=msg, is_answer=is_answer))  # append new content
    return write_session(session)


@app.get("/session/{uuid}")
async def get_session(uuid : str):
    return get_only(uuid)
