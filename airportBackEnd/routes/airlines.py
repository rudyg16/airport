from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from db import get_db_connection

router = APIRouter()

@router.get("/")
def get_airlines():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM airline")
    airlines = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=airlines)

@router.post("/")
def create_airline(airline_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO airline (airline_name) VALUES (%s)", (airline_name,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Airline created successfully"}
