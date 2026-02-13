from sqlalchemy.orm import Session
from app.models import Ticket
from app.utils.ai_client import call_ai_system


def it_agent(ticket: Ticket) -> str:
    prompt = f"""
    You are an IT Support Specialist in a corporate office.
    Provide a short, practical technical resolution.

    Title: {ticket.title}
    Description: {ticket.description}
    """

    return call_ai_system(prompt)


def hr_agent(ticket: Ticket) -> str:
    prompt = f"""
    You are an HR representative.
    Respond professionally and empathetically.

    Title: {ticket.title}
    Description: {ticket.description}
    """

    return call_ai_system(prompt)


def security_agent(ticket: Ticket) -> str:
    prompt = f"""
    You are a Corporate Security Officer.
    Provide a formal and policy-focused resolution.

    Title: {ticket.title}
    Description: {ticket.description}
    """

    return call_ai_system(prompt)


def management_agent(ticket: Ticket) -> str:
    prompt = f"""
    You are a Department Manager.
    Provide leadership-oriented and decision-focused guidance.

    Title: {ticket.title}
    Description: {ticket.description}
    """

    return call_ai_system(prompt)


def employee_relations_agent(ticket: Ticket) -> str:
    prompt = f"""
    You are an Employee Relations Specialist.
    Respond professionally, neutrally, and fairly.

    Title: {ticket.title}
    Description: {ticket.description}
    """

    return call_ai_system(prompt)
