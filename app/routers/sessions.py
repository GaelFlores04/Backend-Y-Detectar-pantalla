from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/start", response_model=schemas.SessionResponse)
def start_session(data: schemas.SessionCreate, db: Session = Depends(get_db)):
    session = models.Session(user_id=data.user_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.post("/{session_id}/end")
def end_session(session_id: int, data: schemas.SessionEnd, db: Session = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    session.end_time = datetime.utcnow()
    session.productivity_score = data.productivity_score
    db.commit()
    return {"message": "Sesión finalizada", "session_id": session_id}

@router.get("/{session_id}/movements", response_model=list[schemas.MovementResponse])
def get_movements(session_id: int, db: Session = Depends(get_db)):
    return db.query(models.Movement).filter(models.Movement.session_id == session_id).all()