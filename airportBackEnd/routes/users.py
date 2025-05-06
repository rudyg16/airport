from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import JSONResponse
from db import get_db_connection

router = APIRouter()

@router.post("/login")
def login_user(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user["user_id"]}

@router.post("/register")
def register_user(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Check for duplicate username
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Username already taken")

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        user_id = cursor.lastrowid

        # Create default passenger (same username for names, dummy info)
        cursor.execute("""
            INSERT INTO passenger (pass_lname, pass_fname, pass_passportID, state_ID, pass_email, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            username.capitalize(),  # last name
            username.capitalize(),  # first name
            f"P{user_id:05}",       # e.g. P00001
            "TX123456",             # dummy state ID
            f"{username}@example.com",  # dummy email
            user_id
        ))
        passenger_id = cursor.lastrowid

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()

    return {
        "message": "User and default passenger created",
        "user_id": user_id,
        "passenger_id": passenger_id
    }


@router.get("/{user_id}/flights")
def get_all_flights_for_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.*
        FROM flight f
        JOIN ticket t ON f.flight_num = t.flight_num
        JOIN passenger p ON p.pass_id = t.ticket_id
        WHERE p.user_id = %s
    """, (user_id,))
    flights = cursor.fetchall()
    for f in flights:
        for k in ["depart_time", "arrival_time"]:
            if f.get(k):
                f[k] = str(f[k])
    cursor.close()
    conn.close()
    return JSONResponse(content=flights)
