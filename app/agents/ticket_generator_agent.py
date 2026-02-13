import random
from sqlalchemy.orm import Session
from app.models import Ticket
from app.utils.ai_client import call_ai_system


CATEGORIES = [
    "IT",
    "HR",
    "Security",
    "Management",
    "Employee Relations"
]


def generate_ticket(db: Session):
    # Randomly choose category
    category = random.choice(CATEGORIES)

    # Build AI prompt
    prompt = f"""
    You are simulating a realistic corporate office environment.

    Generate a realistic support ticket for the {category} department.

    Provide:
    1. A short professional title (max 10 words)
    2. A detailed description (2–4 sentences)

    Format strictly like:
    Title: <title here>
    Description: <description here>
    """

    ai_response = call_ai_system(prompt)

    # Basic parsing
    title = "Generated Ticket"
    description = ai_response

    if "Title:" in ai_response and "Description:" in ai_response:
        try:
            title_part = ai_response.split("Title:")[1].split("Description:")[0].strip()
            description_part = ai_response.split("Description:")[1].strip()

            title = title_part
            description = description_part
        except Exception:
            pass  # fallback to raw response

    # Create ticket
    ticket = Ticket(
        title=title,
        description=description,
        category=category,
        status="OPEN"
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket
