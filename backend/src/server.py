from fastapi import FastAPI

from service import *
from data import *
from service import get_or_create

app = FastAPI()

@app.post("/submit")
async def submit(msg: str, source: str, is_answer: bool, uuid: Optional[str] = None) -> Session:
    session = get_or_create(uuid)
    session.content += Message(name=source, content=msg, is_answer=is_answer)  # append new content
    return write_session(session)


@app.get("/session{uuid}")
async def get_session(uuid : str):
    return get_only(uuid)
