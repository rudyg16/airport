from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from db import get_db_connection
from datetime import datetime

router = APIRouter()


@router.get("/upcoming")
def get_upcoming_flights():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        SELECT * FROM flight
        WHERE depart_time > %s
        ORDER BY depart_time
        LIMIT 8
    """, (now,))
    flights = cursor.fetchall()
    for f in flights:
        for k in ["depart_time", "arrival_time"]:
            if f.get(k):
                f[k] = str(f[k])
    cursor.close()
    conn.close()
    return JSONResponse(content=flights)

@router.get("/search")
def search_flights(
    arrival_city: Optional[str] = None,
    depart_city: Optional[str] = None,
    airline_name: Optional[str] = None,
    date: Optional[str] = None,  # format: 'YYYY-MM-DD'
    min_depart_time: Optional[str] = None  # format: 'HH:MM:SS'
):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = '''SELECT flight.*, model.capacity, airline.airline_name
    FROM flight 
    JOIN airplane ON flight.airplane_id = airplane.airplane_id
    JOIN model ON airplane.model_name = model.model_name 
    JOIN airline ON airplane.airline_name = airline.airline_name
    WHERE 1=1
    '''
    params = []

    if arrival_city:
        query += " AND flight.arrival_city LIKE %s"
        params.append(f"%{arrival_city}%")
    if depart_city:
        query += " AND flight.depart_city LIKE %s"
        params.append(f"%{depart_city}%")
    if airline_name:
        query += " AND airline.airline_name = %s"
        params.append(airline_name)
    if date:
        query += " AND DATE(flight.depart_time) = %s"
        params.append(date)
    if min_depart_time:
        query += " AND TIME(flight.depart_time) >= %s"
        params.append(min_depart_time)

    cursor.execute(query, tuple(params))
    flights = cursor.fetchall()

    for f in flights:
        for k in ["depart_time", "arrival_time"]:
            if f.get(k) and isinstance(f[k], datetime):
                f[k] = f[k].isoformat()

    cursor.close()
    conn.close()
    return JSONResponse(content=flights)



@router.get("/")
def get_flights():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM flight")
    flights = cursor.fetchall()
    for f in flights:
        for k in ["depart_time", "arrival_time"]:
            if f.get(k):
                f[k] = str(f[k])
    cursor.close()
    conn.close()
    return JSONResponse(content=flights)

@router.get("/{flight_num}")
def get_flight_by_number(flight_num: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM flight WHERE flight_num = %s", (flight_num,))
    flight = cursor.fetchone()
    if flight:
        for k in ["depart_time", "arrival_time"]:
            if flight.get(k):
                flight[k] = str(flight[k])
    cursor.close()
    conn.close()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return JSONResponse(content=flight)

@router.post("/")
def create_flight(depart_time: str, arrival_time: str, capacity: int, state_ID: str, pass_email: str, airline_name: str,
                  gate_num: int, terminal_letter: str, arrival_city: str, depart_city: str,
                  arrival_country: str, depart_country: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO flight (depart_time, arrival_time, capacity, state_ID, pass_email, airline_name,
                gate_num, terminal_letter, arrival_city, depart_city, arrival_country, depart_country)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (depart_time, arrival_time, capacity, state_ID, pass_email, airline_name,
              gate_num, terminal_letter, arrival_city, depart_city, arrival_country, depart_country))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Flight created successfully"}

@router.get("/by-user/{user_id}")
def get_tickets_by_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT t.ticket_id, t.seat_num, t.flight_num, f.depart_city, f.arrival_city,
                   f.depart_time, f.arrival_time, f.airline_name, p.pass_fname, p.pass_lname,
                   l.weight, l.bagtype
            FROM ticket t
            JOIN passenger p ON t.pass_id = p.pass_id
            JOIN flight f ON f.flight_num = t.flight_num
            LEFT JOIN luggage l ON l.ticket_id = t.ticket_id
            WHERE p.user_id = %s
        """, (user_id,))
        rows = cursor.fetchall()

        # Group by ticket
        grouped = {}
        for row in rows:
            tid = row["ticket_id"]
            if tid not in grouped:
                grouped[tid] = {
                    "ticket_id": tid,
                    "seat_num": row["seat_num"],
                    "flight": {
                        "flight_num": row["flight_num"],
                        "departureCity": row["depart_city"],
                        "arrivalCity": row["arrival_city"],
                        "depart_time": str(row["depart_time"]),
                        "arrival_time": str(row["arrival_time"]),
                        "airline": row["airline_name"],
                    },
                    "passenger": {
                        "name": f"{row['pass_fname']} {row['pass_lname']}"
                    },
                    "baggage": [],
                }
            if row["weight"] is not None:
                grouped[tid]["baggage"].append({
                    "type": row["bagtype"],
                    "weight": row["weight"],
                })

        return list(grouped.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
