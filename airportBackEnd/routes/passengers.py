from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from db import get_db_connection
from typing import Optional

router = APIRouter()

@router.get("/")
def get_passengers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM passenger")
    passengers = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=passengers)

@router.get("/{passport_id}")
def get_passenger_by_passport(passport_id: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM passenger WHERE pass_passportID = %s", (passport_id,))
    passenger = cursor.fetchone()
    cursor.close()
    conn.close()
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    return JSONResponse(content=passenger)

@router.get("/{passenger_id}/flights")
def get_flights_for_passenger(passenger_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.*
        FROM flight f
        JOIN ticket t ON f.flight_num = t.flight_num
        JOIN passenger p ON p.pass_id = t.ticket_id
        WHERE p.pass_id = %s
    """, (passenger_id,))
    flights = cursor.fetchall()
    for f in flights:
        for k in ["depart_time", "arrival_time"]:
            if f.get(k):
                f[k] = str(f[k])
    cursor.close()
    conn.close()
    return JSONResponse(content=flights)


@router.get("/by-user/{user_id}")
def get_passengers_by_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM passenger WHERE user_id = %s", (user_id,))
    passengers = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=passengers)


@router.post("/")
def create_passenger(pass_lname: str, pass_fname: str, pass_passportID: str, state_ID: str, pass_email: str, user_id: Optional[int] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO passenger (pass_lname, pass_fname, pass_passportID, state_ID, pass_email, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (pass_lname, pass_fname, pass_passportID, state_ID, pass_email, user_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Passenger created successfully"}
