from sqlmodel import create_engine, Session, select
from fastapi import HTTPException, status, Depends
from typing import List
from models import AdminBase, Admin, Employee, AdditionalRoleBase, AdditionalRole, EmployeeAdditionalRoleLink
from datetime import date

import load_env

DATABASE_URL = load_env.get_database_url()
engine = create_engine(DATABASE_URL, echo=True)


# ---------- DB UTILS ----------

def get_session():
    with Session(engine) as session:
        yield session

def get_db():
    with Session(engine) as session:
        yield session


def create_admin_in_db(admin, session):
    if admin.company_name == 'string':
        raise HTTPException(status_code=400, detail="Enter Username")
    if admin.website == 'string':
        raise HTTPException(status_code=400, detail="Enter Email")
    if admin.address == 'string':
        raise HTTPException(status_code=400, detail="Enter password")
    if admin.phone == 'string':
        raise HTTPException(status_code=400, detail="Enter Username")
    if admin.email == 'string':
        raise HTTPException(status_code=400, detail="Enter Email")
    if admin.password == 'string':
        raise HTTPException(status_code=400, detail="Enter password")
    existing = session.exec(
        select(Admin).where(Admin.email == admin.email)).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    db_admin = Admin.model_validate(admin)
    session.add(db_admin)
    session.commit()
    session.refresh(db_admin)
    return db_admin


def update_company_profile_in_db(admin, current_admin, session):
    if admin.company_name != 'string':
        current_admin.company_name = admin.company_name
    if admin.website != 'string':
        current_admin.website = admin.website
    if admin.address != 'string':
        current_admin.address = admin.address
    if admin.phone != 'string':
        current_admin.phone = admin.phone
    if admin.email != 'string':
        current_admin.email = admin.email
    
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return admin


def update_password_in_db(old, new, current_admin, session):
    if old == current_admin.password:
        current_admin.password = new
        session.add(current_admin)
        session.commit()
        session.refresh(current_admin)
        return "Password Update"
    else:
        raise HTTPException(status_code=400, detail="Not Allowed")


def register_new_employee_in_db(employee, lst, current_admin, session):
    # Validate basic fields
    employee_data = employee.dict()
    required_fields = [
        "employee_id", "name", "bank_name", "bank_account_title",
        "bank_branch_code", "bank_account_number", "bank_iban_number",
        "initial_base_salary", "department", "team", "home_address",
        "email", "password", "designation", "cnic", "date_of_birth"
    ]

    for field in required_fields:
        value = employee_data.get(field)
        if value in ("string", "", None, 0, str(date.today()), date.today()):
            raise HTTPException(status_code=400, detail=f"Enter {field}")

    # Check for existing employee
    existing = session.exec(select(Employee).where(Employee.employee_id == employee.employee_id)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee already exists")

    # Set company and default salary
    employee.company_id = current_admin.id
    if employee.current_base_salary == 0:
        employee.current_base_salary = employee.initial_base_salary

    # Default actual DOB
    if employee.actual_date_of_birth == date.today():
        employee.actual_date_of_birth = employee.date_of_birth

    # Save employee
    addemployee = Employee.model_validate(employee)
    session.add(addemployee)
    session.commit()
    session.refresh(addemployee)

    # Handle additional roles
    for role_data in lst:
        if role_data.role_name == "string":
            break
        role = AdditionalRole.model_validate(role_data)
        session.add(role)
        session.commit()
        session.refresh(role)

        link = EmployeeAdditionalRoleLink(
            employee_id=addemployee.employee_id,
            role_id=role.id
        )
        session.add(link)

    session.commit()
    session.refresh(addemployee)

    return {"message": "Employee Added Successfully", "employee": addemployee}

def update_employee_details_in_db(employee, lst, current_admin, session):
    
    if employee.employee_id == "string":
        raise HTTPException(status_code=400, detail="Enter employee_id")
    
    employee_to_update = session.exec(select(Employee).where(Employee.employee_id == employee.employee_id)).first()
    
    if not employee_to_update:
        raise HTTPException(status_code=400, detail="Employee does not exists")
    
    if employee_to_update.company_id != current_admin.id:
        raise HTTPException(status_code=400, detail="method Not Allowed for this employee")
    
    employee_data = employee.dict(exclude_unset=True, exclude_defaults=True)
    for key, value in employee_data.items():
        if value not in ["string", 0, str(date.today())]:
            setattr(employee_to_update, key, value)

    session.add(employee_to_update)
    session.commit()
    session.refresh(employee_to_update)

    return {"message": "Employee updated successfully", "employee": employee_to_update}
