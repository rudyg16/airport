from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from db import get_db_connection

router = APIRouter()

@router.get("/")
def get_terminals():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM terminal")
    terminals = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=terminals)

@router.get("/gates")
def get_gates():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gate")
    gates = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=gates)

@router.post("/")
def create_terminal(terminal_letter: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO terminal (terminal_letter) VALUES (%s)", (terminal_letter,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Terminal created successfully"}

@router.post("/gates")
def create_gate(gate_num: int, terminal_letter: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO gate (gate_num, terminal_letter) VALUES (%s, %s)", (gate_num, terminal_letter))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Gate created successfully"}
