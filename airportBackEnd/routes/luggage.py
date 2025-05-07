from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from db import get_db_connection

router = APIRouter()

@router.post("/")
def create_luggage(pass_id: int, ticket_id: int, weight: float, bagtype: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO luggage (pass_id, ticket_id, weight, bagtype)
            VALUES (%s, %s, %s, %s)
        """, (pass_id, ticket_id, weight, bagtype))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Luggage added successfully"}

@router.get("/")
def get_luggage(pass_id: Optional[int] = None, ticket_id: Optional[int] = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM luggage WHERE 1=1"
    params = []

    if pass_id is not None:
        query += " AND pass_id = %s"
        params.append(pass_id)
    if ticket_id is not None:
        query += " AND ticket_id = %s"
        params.append(ticket_id)

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=results)

@router.delete("/{luggage_id}")
def delete_luggage(luggage_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM luggage WHERE luggage_id = %s", (luggage_id,))
        conn.commit()
        return JSONResponse(content={"message": "Luggage deleted successfully"})
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
