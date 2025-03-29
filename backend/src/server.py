from fastapi import FastAPI
from typing import Optional

from service import *
from data import *

app = FastAPI()

@app.post("/submit")
async def submit(msg: str, source: str, is_answer: bool, uuid: Optional[str] = None):
    session = get_or_create(uuid)
    session.content += Message(name=source, content=msg, is_answer=is_answer)  # append new content
    write_session(session)
    return QuestionStatus(uuid=session.uuid, estimated_seconds=-1)
