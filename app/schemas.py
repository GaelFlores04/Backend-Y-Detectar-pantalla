from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionCreate(BaseModel):
    user_id: int

class SessionResponse(BaseModel):
    id: int
    user_id: int
    start_time: datetime
    model_config = {"from_attributes": True}

class SessionEnd(BaseModel):
    productivity_score: Optional[float] = None

class MovementResponse(BaseModel):
    id: int
    session_id: int
    timestamp: datetime
    distraction_type: str
    duration: int
    model_config = {"from_attributes": True}