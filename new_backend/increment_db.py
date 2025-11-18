from fastapi import HTTPException
from sqlmodel import select
from datetime import date
from models import EmployeeIncrement, Employee, Company


# ---------------- CREATE ----------------
def create_increment_in_db(new_increment, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    
    employee =  session.exec(select(Employee).where(Employee.employee_id == new_increment.employee_id,
                                                    Employee.company_id == company.company_id)).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee Doesn't Exists")
    
    if employee.company_id != company.company_id:
        raise HTTPException(status_code=403, detail="There is no Employee with given ID")
    
    existing = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == new_increment.employee_id)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Increment already exists")
    
    new_increment = EmployeeIncrement.model_validate(new_increment)
    employee.increment_amount = new_increment.increment_amount
    employee.last_increment_date = new_increment.effective_date
    employee.current_base_salary += new_increment.increment_amount
    session.add(new_increment)
    session.commit()
    session.refresh(new_increment)
    session.refresh(employee)
    return new_increment

# ---------------- READ ----------------
def get_increment_by_id_in_db(employee_id, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    Increment = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == employee_id,
                                                             EmployeeIncrement.company_id == company.company_id)).first()
    if Increment:
        return Increment
    raise HTTPException(status_code=404, detail="Increment does not exist")

# ---------------- UPDATE / EDIT ----------------
def update_increment_in_db(new_increment, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    increment = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == new_increment.employee_id,
                                                             EmployeeIncrement.company_id == company.company_id)).first()
    if not increment:
        raise HTTPException(status_code=404, detail="Increment does not exist")
    employee =  session.exec(select(Employee).where(Employee.employee_id == new_increment.employee_id)).first()
    if new_increment.increment_amount != 0:
        increment.increment_amount = new_increment.increment_amount
        if new_increment.increment_amount >= employee.increment_amount:
            employee.current_base_salary += (new_increment.increment_amount - employee.increment_amount)
        else:
            employee.current_base_salary -= (employee.increment_amount - new_increment.increment_amount)
        employee.increment_amount = new_increment.increment_amount
    if new_increment.effective_date != str(date.today()):
        increment.effective_date = new_increment.effective_date
        employee.last_increment_date = new_increment.effective_date
        
    if new_increment.notes != 'string':
        increment.notes = new_increment.notes

    session.commit()
    session.refresh(increment)
    session.refresh(employee)
    return increment

# ---------------- HARD DELETE ----------------
def delete_increment_in_db(employee_id, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    increment = session.exec(select(EmployeeIncrement).where(EmployeeIncrement.employee_id == employee_id,
                                                             EmployeeIncrement.company_id == company.company_id)).first()
    if not increment:
        raise HTTPException(status_code=404, detail="Increment does not exist")
    
    session.delete(increment)
    session.commit()
    return {"detail": "Increment deleted successfully"}