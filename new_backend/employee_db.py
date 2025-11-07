from sqlmodel import create_engine, Session, select
from fastapi import HTTPException, status, Depends
from typing import List
from models import AdminBase, Admin, Employee, AdditionalRoleBase, AdditionalRole, EmployeeAdditionalRoleLink
from datetime import date

import load_env

DATABASE_URL = load_env.get_database_url()
engine = create_engine(DATABASE_URL, echo=True)


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

    return {"message": "Employee Added Successfully", "employee": addemployee, "Additional Roles": lst}


def update_employee_details_in_db(employee, current_admin, session):
    if employee.employee_id == "string":
        raise HTTPException(status_code=400, detail="Enter employee_id")

    employee_to_update = session.exec(
        select(Employee).where(Employee.employee_id == employee.employee_id)
    ).first()

    if not employee_to_update:
        raise HTTPException(status_code=400, detail="Employee does not exist")

    if employee_to_update.company_id != current_admin.id:
        raise HTTPException(status_code=400, detail="Method not allowed for this employee")

    # --- Update base employee fields ---
    employee_data = employee.dict(exclude_unset=True, exclude_defaults=True)
    for key, value in employee_data.items():
        if value not in ["string", 0, str(date.today())]:
            setattr(employee_to_update, key, value)

    # --- Finalize DB transaction ---
    session.add(employee_to_update)
    session.commit()
    session.refresh(employee_to_update)

    return {"message": "Employee updated successfully", "employee": employee_to_update}


def deactivate_employee_in_db(employee_id, current_admin, session):
    
    if employee_id == "string":
        raise HTTPException(status_code=400, detail="Enter employee_id")

    employee_to_update = session.exec(
        select(Employee).where(Employee.employee_id == employee_id)
    ).first()

    if not employee_to_update:
        raise HTTPException(status_code=400, detail="Employee does not exist")

    if employee_to_update.company_id != current_admin.id:
        raise HTTPException(status_code=400, detail="Method not allowed for this employee")
    
    employee_to_update.status = False
    return {"Mesasage" : "Employee has been Seactivated", "Employee" : employee_to_update.employee_id, "Status": employee_to_update.status}

def display_all_employee(page, page_size, department, team, current_admin, session):
    
    query = select(Employee).where(Employee.company_id == current_admin.id)

    # Apply filters dynamically
    if department:
        query = query.where(Employee.department.ilike(f"%{department}%"))
    if team:
        query = query.where(Employee.team.ilike(f"%{team}%"))

    # Pagination
    total_employees = session.exec(query).all()
    total_count = len(total_employees)

    offset = (page - 1) * page_size
    paginated_employees = total_employees[offset:offset + page_size]

    if not paginated_employees:
        raise HTTPException(status_code=404, detail="No employees found for this query")

    # Return structured response
    return {
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": (total_count + page_size - 1) // page_size,
        "filters": {
            "department": department or "All",
            "team": team or "All",
        },
        "employees": paginated_employees,
    }
    
# Under Working
def update_roles_in_db(employee_id, lst, current_admin, session):
    if employee_id == "string":
        raise HTTPException(status_code=400, detail="Enter employee_id")

    employee_to_update = session.exec(
        select(Employee).where(Employee.employee_id == employee_id)
    ).first()

    if not employee_to_update:
        raise HTTPException(status_code=400, detail="Employee does not exist")

    if employee_to_update.company_id != current_admin.id:
        raise HTTPException(status_code=400, detail="Method not allowed for this employee")
    # --- Handle roles logic ---
    for role_data in lst:
        role_to_update = session.exec(
            select(AdditionalRole).where(AdditionalRole.role_name == role_data.role_name)
        ).first()

        if not role_to_update:
            raise HTTPException(
                status_code=404,
                detail=f"Role '{role_data.role_name}' not found for update"
            )

        if role_data.role_description and role_data.role_description != "string":
            role_to_update.role_description = role_data.role_description

        session.add(role_to_update)
    
    
    return {"message": "Role updated successfully", "Roles": lst}