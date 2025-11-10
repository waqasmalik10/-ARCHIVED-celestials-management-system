from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import Session, select
from datetime import date
from models import EmployeeIncrement

# Under Working..............

# ---------------- CREATE ----------------
def create_increment_in_db(new_increment, session):
    existing = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == new_increment.employee_id)).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Employee already exists")
    
    session.add(new_increment)
    session.commit()
    session.refresh(new_increment)
    return new_increment

# ---------------- READ ----------------
def get_increments_in_db(employee_id, session) -> List[EmployeeIncrement]:
    Increment = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == employee_id)).first()
    if Increment:
        return Increment
    raise HTTPException(status_code=400, detail="Increment does not exist")

# ---------------- UPDATE / EDIT ----------------
def update_increment_in_db(new_increment, session):
    Increment = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == new_increment.employee_id)).first()
    if not Increment:
        raise HTTPException(status_code=400, detail="Employee does not exist")
    
    if new_increment.increment_amount != 0:
        Increment.increment_amount = new_increment.increment_amount
    if new_increment.effective_date != str(date.today()):
        Increment.effective_date = new_increment.effective_date
    if new_increment.notes != str:
        Increment.notes = new_increment.notes

    session.commit()
    session.refresh(Increment)
    return Increment

# ---------------- HARD DELETE ----------------
def delete_increment_in_db(employee_id, session):
    increment = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == employee_id)).first()
    if not increment:
        raise HTTPException(status_code=400, detail="Employee does not exist")
    
    session.delete(increment)
    session.commit()
    return {"detail": "Increment deleted successfully"}
