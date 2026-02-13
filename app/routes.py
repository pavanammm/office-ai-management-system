# API routes will go here
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Ticket, TicketCreate, TicketResponse
from app.agents.resolver_agent import process_next_ticket, process_ticket_background
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
def create_ticket(
    ticket: TicketCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        category=ticket.category,
        status="OPEN"
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    # Trigger background processing
    background_tasks.add_task(process_ticket_background)

    return new_ticket



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
def create_generated_ticket(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    ticket = generate_ticket(db)

    background_tasks.add_task(process_ticket_background)

    return ticket
