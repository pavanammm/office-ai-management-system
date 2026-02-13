# Database models will go here
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import Literal

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    status = Column(String, default="OPEN")
    resolution = Column(String, nullable=True)   # NEW FIELD
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)




class TicketCreate(BaseModel):
    title: str
    description: str
    category: Literal[
        "IT",
        "HR",
        "Security",
        "Management",
        "Employee Relations"
    ]


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    status: str
    resolution: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
