from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app import models
from app.database import get_db

router = APIRouter(tags=["activity"])

def parse_timestamp(raw: str) -> datetime:
    # Formato esperado: "2026-04-13|14:35:22"
    return datetime.strptime(raw, "%Y-%m-%d|%H:%M:%S")

@router.websocket("/ws/activity/{session_id}")
async def activity_websocket(
    websocket: WebSocket,
    session_id: int,
    db: Session = Depends(get_db)
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # data esperado: {"timestamp": "2026-04-13|14:35:22", "duration": 63}
            movement = models.Movement(
                session_id=session_id,
                timestamp=parse_timestamp(data["timestamp"]),
                distraction_type="inactivity",
                duration=data["duration"]
            )
            db.add(movement)
            db.commit()
            await websocket.send_json({"status": "ok", "movement_id": movement.id})
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"status": "error", "detail": str(e)})