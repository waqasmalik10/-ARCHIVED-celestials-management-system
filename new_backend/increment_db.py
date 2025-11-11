from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import Session, select
from datetime import date
from models import EmployeeIncrement, Employee

# Under Working..............

# ---------------- CREATE ----------------
def create_increment_in_db(new_increment, session):
    existing = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == new_increment.employee_id)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee already exists")
    new_increment = EmployeeIncrement.model_validate(new_increment)
    employee =  session.exec(select(Employee).where(Employee.employee_id == new_increment.employee_id)).first()
    employee.increment_amount = new_increment.increment_amount
    employee.last_increment_date = new_increment.effective_date
    employee.current_base_salary += new_increment.increment_amount
    session.add(new_increment)
    session.commit()
    session.refresh(new_increment)
    session.refresh(employee)
    return new_increment

# ---------------- READ ----------------
def get_increments_in_db(employee_id, session) -> List[EmployeeIncrement]:
    Increment = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == employee_id)).first()
    if Increment:
        return Increment
    raise HTTPException(status_code=400, detail="Increment does not exist")

# ---------------- UPDATE / EDIT ----------------
def update_increment_in_db(new_increment, session):
    increment = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == new_increment.employee_id)).first()
    if not increment:
        raise HTTPException(status_code=400, detail="Increment does not exist")
    employee =  session.exec(select(Employee).where(Employee.employee_id == new_increment.employee_id)).first()
    if new_increment.increment_amount != 0:
        increment.increment_amount = new_increment.increment_amount
        employee.increment_amount = new_increment.increment_amount
        employee.current_base_salary += new_increment.increment_amount
    if new_increment.effective_date != str(date.today()):
        increment.effective_date = new_increment.effective_date
        employee.last_increment_date = new_increment.effective_date
        
    if new_increment.notes != str:
        increment.notes = new_increment.notes

    session.commit()
    session.refresh(increment)
    session.refresh(employee)
    return increment

# ---------------- HARD DELETE ----------------
def delete_increment_in_db(employee_id, session):
    increment = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == employee_id)).first()
    if not increment:
        raise HTTPException(status_code=400, detail="Increment does not exist")
    
    session.delete(increment)
    session.commit()
    session.refresh(increment)
    return {"detail": "Increment deleted successfully"}