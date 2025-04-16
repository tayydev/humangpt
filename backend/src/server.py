from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from service import *
from data import *
from service import get_or_create_session
from sockets import *

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


@app.get("/get-session")
async def session_endpoint(uuid: str) -> SessionDTO:
    return get_session(uuid).to_dto()  # no messages


@app.get("/all-unanswered-sessions")
async def all_unanswered_sessions(answerer_id: str) -> list[Session]:
    return sorted(
        [s for s in get_sessions_list() if not s.content[-1].is_answer and s.user_id != answerer_id],
        key=lambda s: s.updated_timestamp
    )

@app.get("/all-sessions")
async def all_sessions() -> list[Session]:
    return get_sessions_list()

@app.post("/guest-user")
async def guest() -> UserPublic:
    return create_temp_user()

@app.get("/get-user")
async def get_user(uuid: str):
    return get_user(uuid)

@app.post("/create-session")
async def create_session(title: str, user_id: str) -> SessionDTO:
    return write_session(get_or_create_session(None, title, user_id)).to_dto()

# websockets
@app.websocket("/ws/session")
async def ws_session(websocket: WebSocket, session_id: str):
    print("New session requested!")

    await socket_manager.connect(websocket)

    try:
        # catch-up
        await catch_up_socket(websocket, session_id)

        print("Session got caught up!")

        while True:
            data = await websocket.receive_json()
            msg: Message = Message.model_validate(data)
            await append_to_session(session_id, msg)

    except WebSocketDisconnect:
        socket_manager.disconnect(websocket)

