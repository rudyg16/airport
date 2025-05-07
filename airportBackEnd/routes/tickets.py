from fastapi import APIRouter, HTTPException, Request
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
def create_ticket(flight_num: int, pass_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT MAX(seat_num) AS max_seat FROM ticket WHERE flight_num = %s", (flight_num,))
        result = cursor.fetchone()
        current_max = result["max_seat"] or 0

        cursor.execute("""
            SELECT m.capacity
            FROM flight f
            JOIN airplane a ON f.airplane_id = a.airplane_id
            JOIN model m ON a.model_name = m.model_name
            WHERE f.flight_num = %s
        """, (flight_num,))
        model = cursor.fetchone()

        if not model:
            raise HTTPException(status_code=404, detail="Flight not found")

        capacity = model["capacity"]
        if current_max >= capacity:
            raise HTTPException(status_code=400, detail="Flight is fully booked")

        seat_num = current_max + 1
        cursor.execute(
            "INSERT INTO ticket (seat_num, flight_num, pass_id) VALUES (%s, %s, %s)",
            (seat_num, flight_num, pass_id)
        )
        ticket_id = cursor.lastrowid
        conn.commit()
        return JSONResponse(content={
            "ticket_id": ticket_id,
            "seat_num": seat_num,
            "flight_num": flight_num,
            "pass_id": pass_id
        })
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/book")
def book_ticket(request: Request):
    params = request.query_params
    flight_num = int(params.get("flight_num"))
    passenger_id = int(params.get("passenger_id"))
    baggage = params.getlist("baggage")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT MAX(seat_num) AS max_seat FROM ticket WHERE flight_num = %s", (flight_num,))
        result = cursor.fetchone()
        current_max = result["max_seat"] or 0

        cursor.execute("""
            SELECT m.capacity
            FROM flight f
            JOIN airplane a ON f.airplane_id = a.airplane_id
            JOIN model m ON a.model_name = m.model_name
            WHERE f.flight_num = %s
        """, (flight_num,))
        model = cursor.fetchone()

        if not model:
            raise HTTPException(status_code=404, detail="Flight not found")

        capacity = model["capacity"]
        if current_max >= capacity:
            raise HTTPException(status_code=400, detail="Flight is fully booked")

        seat_num = current_max + 1
        cursor.execute(
            "INSERT INTO ticket (seat_num, flight_num, pass_id) VALUES (%s, %s, %s)",
            (seat_num, flight_num, passenger_id)
        )
        ticket_id = cursor.lastrowid

        # attach baggage
        for item in baggage:
            bag = eval(item)
            cursor.execute(
                "INSERT INTO luggage (pass_id, ticket_id, weight, bagtype) VALUES (%s, %s, %s, %s)",
                (passenger_id, ticket_id, bag["weight"], bag["bagtype"]) 
            )

        conn.commit()
        return JSONResponse(content={
            "ticket_id": ticket_id,
            "seat_num": seat_num,
            "flight_num": flight_num,
            "passenger_id": passenger_id
        })
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
@router.get("/by-user/{user_id}")
def get_tickets_by_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT
                t.ticket_id,
                t.seat_num,
                t.flight_num,
                f.depart_city,
                f.arrival_city,
                f.depart_time,
                f.arrival_time,
                al.airline_name,           -- grab it from airline
                p.pass_fname,
                p.pass_lname,
                l.weight,
                l.bagtype
            FROM ticket t
            JOIN passenger p  ON t.pass_id      = p.pass_id
            JOIN flight    f  ON f.flight_num   = t.flight_num
            JOIN airplane  ap ON f.airplane_id  = ap.airplane_id
            JOIN airline   al ON ap.airline_name = al.airline_name
            LEFT JOIN luggage  l ON l.ticket_id   = t.ticket_id
            WHERE p.user_id = %s
        """, (user_id,))
        rows = cursor.fetchall()

        grouped = {}
        for row in rows:
            tid = row["ticket_id"]
            if tid not in grouped:
                grouped[tid] = {
                    "ticket_id": tid,
                    "seat_num": row["seat_num"],
                    "flight": {
                        "flight_num":      row["flight_num"],
                        "departureCity":   row["depart_city"],
                        "arrivalCity":     row["arrival_city"],
                        "depart_time":     row["depart_time"].isoformat()  if hasattr(row["depart_time"],   "isoformat") else str(row["depart_time"]),
                        "arrival_time":    row["arrival_time"].isoformat() if hasattr(row["arrival_time"], "isoformat") else str(row["arrival_time"]),
                        "airline":         row["airline_name"],
                    },
                    "passenger": {"name": f"{row['pass_fname']} {row['pass_lname']}"},
                    "baggage": []
                }
            if row["weight"] is not None:
                grouped[tid]["baggage"].append({
                    "type":   row["bagtype"],
                    "weight": row["weight"],
                })

        return list(grouped.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM luggage WHERE ticket_id = %s", (ticket_id,))
        cursor.execute("DELETE FROM ticket WHERE ticket_id = %s", (ticket_id,))
        conn.commit()
        return JSONResponse(content={"message": "Deleted ticket and baggage"})
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
