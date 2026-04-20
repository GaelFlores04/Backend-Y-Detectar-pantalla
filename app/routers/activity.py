from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app import models
from app.database import get_db

router = APIRouter(tags=["activity"])

@router.websocket("/ws/activity/{session_id}")
async def activity_websocket(
    websocket: WebSocket,
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            movement = models.Movement(
                session_id=session_id,
                timestamp=datetime.strptime(data["timestamp"], "%Y-%m-%d|%H:%M:%S"),
                distraction_type="inactivity",
                duration=data["duration"]
            )
            db.add(movement)
            await db.commit()
            await websocket.send_json({"status": "ok", "movement_id": movement.id})
    except WebSocketDisconnect:
        pass