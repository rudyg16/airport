from fastapi import APIRouter, HTTPException
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


@router.get("/by-user/{user_id}")
def get_passengers_by_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM passenger WHERE user_id = %s", (user_id,))
    passengers = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=passengers)


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


@router.post("/")
def create_passenger(
    pass_lname: str,
    pass_fname: str,
    pass_passportID: str,
    state_ID: str,
    pass_email: str,
    user_id: int  # required
):
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


@router.patch("/{pass_id}")
def update_passenger(
    pass_id: int,
    user_id: int,  # required to validate ownership
    pass_lname: Optional[str] = None,
    pass_fname: Optional[str] = None,
    pass_passportID: Optional[str] = None,
    state_ID: Optional[str] = None,
    pass_email: Optional[str] = None
):
    fields = []
    values = []

    if pass_lname:
        fields.append("pass_lname = %s")
        values.append(pass_lname)
    if pass_fname:
        fields.append("pass_fname = %s")
        values.append(pass_fname)
    if pass_passportID:
        fields.append("pass_passportID = %s")
        values.append(pass_passportID)
    if state_ID:
        fields.append("state_ID = %s")
        values.append(state_ID)
    if pass_email:
        fields.append("pass_email = %s")
        values.append(pass_email)

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.extend([pass_id, user_id])

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            UPDATE passenger
            SET {', '.join(fields)}
            WHERE pass_id = %s AND user_id = %s
        """, tuple(values))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Passenger not found or unauthorized")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    return {"message": f"Passenger {pass_id} updated successfully"}


@router.delete("/{pass_id}")
def delete_passenger(pass_id: int, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM passenger WHERE pass_id = %s AND user_id = %s", (pass_id, user_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Passenger not found or not owned by this user")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    return {"message": f"Passenger {pass_id} deleted successfully"}
