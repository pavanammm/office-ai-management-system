from sqlalchemy.orm import Session
from app.models import Ticket
from app.agents.department_agents import (
    it_agent,
    hr_agent,
    security_agent,
    management_agent,
    employee_relations_agent,
)


def process_next_ticket(db: Session):
    ticket = db.query(Ticket).filter(Ticket.status == "OPEN").first()

    if not ticket:
        return {"message": "No open tickets found"}

    # Route based on category
    if ticket.category == "IT":
        resolution = it_agent(ticket)

    elif ticket.category == "HR":
        resolution = hr_agent(ticket)

    elif ticket.category == "Security":
        resolution = security_agent(ticket)

    elif ticket.category == "Management":
        resolution = management_agent(ticket)

    elif ticket.category == "Employee Relations":
        resolution = employee_relations_agent(ticket)

    else:
        resolution = "No appropriate department found."

    ticket.status = "RESOLVED"
    ticket.resolution = resolution

    db.commit()
    db.refresh(ticket)

    return ticket
