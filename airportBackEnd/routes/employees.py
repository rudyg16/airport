from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from db import get_db_connection

router = APIRouter()

@router.get("/")
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=employees)

@router.get("/{employee_id}")
def get_employee_by_id(employee_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee WHERE employ_id = %s", (employee_id,))
    employee = cursor.fetchone()
    cursor.close()
    conn.close()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return JSONResponse(content=employee)

@router.post("/")
def create_employee(employ_ssn: str, job_role: str, employ_fname: str, employ_lname: str, airline_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO employee (employ_ssn, job_role, employ_fname, employ_lname, airline_name)
            VALUES (%s, %s, %s, %s, %s)
        """, (employ_ssn, job_role, employ_fname, employ_lname, airline_name))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Employee created successfully"}
