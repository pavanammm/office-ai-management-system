# API routes will go here
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Ticket, TicketCreate, TicketResponse
from app.agents.resolver_agent import process_next_ticket
from app.agents.ticket_generator_agent import generate_ticket


router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/tickets", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        category=ticket.category
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
@router.get("/tickets", response_model=list[TicketResponse])
def get_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()
@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
@router.put("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket_status(ticket_id: int, status: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = status
    db.commit()
    db.refresh(ticket)
    return ticket
@router.post("/process-next-ticket")
def process_ticket(db: Session = Depends(get_db)):
    result = process_next_ticket(db)
    return result

@router.post("/generate-ticket")
def create_generated_ticket(db: Session = Depends(get_db)):
    ticket = generate_ticket(db)
    return ticket