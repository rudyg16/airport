from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from db import get_db_connection

router = APIRouter()

@router.get("/")
def get_tickets():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ticket")
    tickets = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=tickets)

@router.get("/{ticket_id}")
def get_ticket_by_id(ticket_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ticket WHERE ticket_id = %s", (ticket_id,))
    ticket = cursor.fetchone()
    cursor.close()
    conn.close()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return JSONResponse(content=ticket)

@router.post("/")
def create_ticket(seat_num: int, flight_num: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO ticket (seat_num, flight_num)
            VALUES (%s, %s)
        """, (seat_num, flight_num))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Ticket created successfully"}

@router.post("/book")
def book_ticket(seat_num: int, flight_num: int, passenger_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if seat already exists for the flight
        cursor.execute("""
            SELECT * FROM ticket WHERE flight_num = %s AND seat_num = %s
        """, (flight_num, seat_num))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Seat already taken on this flight")

        cursor.execute("""
            INSERT INTO ticket (seat_num, flight_num)
            VALUES (%s, %s)
        """, (seat_num, flight_num))
        ticket_id = cursor.lastrowid


        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Ticket booked successfully", "ticket_id": ticket_id}
