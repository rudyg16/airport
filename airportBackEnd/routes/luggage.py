from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from db import get_db_connection

router = APIRouter()

@router.post("/")
def create_luggage(pass_id: int, flight_num: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO luggage (pass_id, flight_num)
            VALUES (%s, %s)
        """, (pass_id, flight_num))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Luggage added successfully"}

@router.get("/")
def get_luggage(pass_id: Optional[int] = None, flight_num: Optional[int] = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM luggage WHERE 1=1"
    params = []

    if pass_id:
        query += " AND pass_id = %s"
        params.append(pass_id)
    if flight_num:
        query += " AND flight_num = %s"
        params.append(flight_num)

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=results)
