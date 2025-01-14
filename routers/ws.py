from fastapi import APIRouter, WebSocket, Query
from starlette.websockets import WebSocketDisconnect
from typing import Optional
import jwt
from core.config import settings

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_message(self, message: str, websocket: WebSocket):
        for connection in self.connections:
            if connection == websocket:
                continue

            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket('/ws')
async def websocket(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
    client: Optional[str] = Query("anonymous"),
):
    if not token:
        await websocket.close(code=1008)
        return
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username = payload.get("sub")
    except jwt.ExpiredSignatureError:
        await websocket.close(code=4401)
        return
    except jwt.InvalidTokenError:
        await websocket.close(code=4403)
        return

    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"{username}(You): " + data, websocket)
            await manager.broadcast_message(f"{username}: " + data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_message(f"{username or client} disconnected", websocket)
