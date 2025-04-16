from starlette.websockets import WebSocket

from data import *
from service import *

async def catch_up_socket(socket: WebSocket, session_id: str):
    all_messages = get_session(session_id).content
    await socket.send_json([m.model_dump_json() for m in all_messages])


class SessionSocketManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}  # map uuid -> socket

    async def connect(self, websocket: WebSocket, session_uuid: str):
        await websocket.accept()
        self.active[session_uuid] = websocket

    def disconnect(self, websocket: WebSocket):
        for session_uuid, socket in list(self.active.items()):
            if socket == websocket:
                self.active.pop(session_uuid)
                break

    async def update_session(self, session_id: str, message: Message):
        for session_uuid, socket in list(self.active.items()):
            if session_uuid == session_id:
                # we always update session as a list
                await socket.send_json([message.model_dump_json()])



socket_manager = SessionSocketManager()
