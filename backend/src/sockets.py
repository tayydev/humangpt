import json

from starlette.websockets import WebSocket

from data import Message

async def catch_up_socket(socket: WebSocket, session_id: str, _user_id: str) -> bool:
    from gpt_service import get_session
    try:
        all_messages = get_session(session_id).content
    except Exception:
        return False  # failed to catch up socket
    await socket.send_json([json.loads(m.model_dump_json()) for m in all_messages])
    return True


class SessionSocketManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}  # map session_uuid+user_uuid -> socket  # TODO: this is bad lol it breaks multiple logins from the same user

    async def connect(self, websocket: WebSocket, session_uuid: str, user_id: str):
        await websocket.accept()
        self.active[session_uuid + user_id] = websocket

    def disconnect(self, websocket: WebSocket):
        for combined_uuid, socket in list(self.active.items()):
            if socket == websocket:
                self.active.pop(combined_uuid)
                break

    async def update_session(self, session_id: str, user_id: str, message: Message):
        for combined_uuid, socket in list(self.active.items()):
            if session_id in combined_uuid:  # important that we hit everyone here
                print("Broadcasting message now")
                # we always update session as a list
                await socket.send_json([json.loads(message.model_dump_json())])



socket_manager = SessionSocketManager()
