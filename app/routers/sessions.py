from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/start", response_model=schemas.SessionResponse)
async def start_session(data: schemas.SessionCreate, db: AsyncSession = Depends(get_db)):
    session = models.Session(user_id=data.user_id)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

@router.post("/{session_id}/end")
async def end_session(session_id: int, data: schemas.SessionEnd, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Session).where(models.Session.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    session.end_time = datetime.utcnow()
    session.productivity_score = data.productivity_score
    await db.commit()
    return {"message": "Sesión finalizada", "session_id": session_id}

@router.get("/{session_id}/movements", response_model=list[schemas.MovementResponse])
async def get_movements(session_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Movement).where(models.Movement.session_id == session_id))
    return result.scalars().all()