from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from datetime import datetime

# Fake in-memory database (this would be replaced with a real database in production)
fake_db = {}

app = FastAPI()

# Root endpoint for a simple welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to the Bus Booking System API!"}

# Models for request and response
class TicketRequest(BaseModel):
    origin: str
    destination: str
    date: datetime
    price: float
    seat_number: str

class TicketResponse(BaseModel):
    ticket_id: str
    origin: str
    destination: str
    seat_number: str
    price: float
    status: str
    booking_date: datetime

# Endpoint to search for tickets based on origin and destination
@app.get("/search")
def search_tickets(origin: str, destination: str):
    # In a real system, this would query the database for available tickets
    available_tickets = [ticket for ticket in fake_db.values() if ticket["origin"] == origin and ticket["destination"] == destination]
    return available_tickets

# Endpoint to book a ticket
@app.post("/book", response_model=TicketResponse)
def book_ticket(ticket: TicketRequest):
    # Prevent booking if the price is incorrect (server side ensures pricing)
    if ticket.price < 0:
        raise HTTPException(status_code=400, detail="Invalid ticket price")
    
    ticket_id = str(uuid4())  # Generate a unique ticket ID
    fake_db[ticket_id] = {
        "ticket_id": ticket_id,
        "origin": ticket.origin,
        "destination": ticket.destination,
        "seat_number": ticket.seat_number,
        "price": ticket.price,
        "status": "BOOKED",  # Initially, it's booked
        "booking_date": datetime.utcnow(),
    }

    return fake_db[ticket_id]

# Endpoint to cancel a booking
@app.delete("/cancel/{ticket_id}", response_model=TicketResponse)
def cancel_ticket(ticket_id: str):
    if ticket_id not in fake_db:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket = fake_db[ticket_id]
    ticket["status"] = "CANCELLED"
    return ticket
