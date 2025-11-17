from sqlmodel import create_engine, select
from pydantic import field_validator
from fastapi import HTTPException
from models import Employee, Company, AdditionalRole, EmployeeAdditionalRoleLink
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

    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    # Check for existing employee
    existing = session.exec(
        select(Employee).where(Employee.employee_id == employee.employee_id, Employee.company_id == company.company_id)
        ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Employee already exists")

    # Set default salary
    if employee.current_base_salary == 0:
        employee.current_base_salary = employee.initial_base_salary

    # Default actual DOB
    if employee.actual_date_of_birth == date.today():
        employee.actual_date_of_birth = employee.date_of_birth

    # Save employee
    employee = Employee.model_validate(employee)
    employee.company_id = company.company_id
    session.add(employee)
    session.commit()
    session.refresh(employee)

    # Handle additional roles
    for role_data in lst:
        if role_data.role_name == "string":
            break
        role = AdditionalRole.model_validate(role_data)
        session.add(role)
        session.commit()

        link = EmployeeAdditionalRoleLink(
            employee_id=employee.employee_id,
            role_id=role.id
        )
        session.add(link)
        session.commit()
        session.refresh(role)

    
    session.commit()
    session.refresh(employee)

    return {"message": "Employee Added Successfully", "employee": employee.employee_id}

def update_employee_details_in_db(employee, current_admin, session):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    # Check for existing employee
    employee_to_update = session.exec(
        select(Employee).where(Employee.employee_id == employee.employee_id, Employee.company_id == company.company_id)).first()

    if not employee_to_update:
        raise HTTPException(status_code=404, detail="Employee does not exist")

    if not employee_to_update.status:
        raise HTTPException(status_code=404, detail="Employee is deativated")
    
    if employee_to_update.company_id != company.company_id:
        raise HTTPException(status_code=403, detail="Method not allowed for this employee because you are not admin of this employee")

    # --- Update base employee fields ---
    employee_data = employee.dict(exclude_unset=True, exclude_defaults=True)
    for key, value in employee_data.items():
        if value not in ["string", 0, str(date.today())]:
            setattr(employee_to_update, key, value)

    # --- Finalize DB transaction ---
    session.commit()
    session.refresh(employee_to_update)

    return {"message": "Employee updated successfully", "employee": employee_to_update}

def deactivate_employee_in_db(employee_id, current_admin, session):
    if employee_id == "string":
        raise HTTPException(status_code=400, detail="Enter employee_id")

    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    # Check for existing employee
    employee_to_update = session.exec(
        select(Employee).where(Employee.employee_id == employee_id, Employee.company_id == company.company_id)).first()
    
    if not employee_to_update:
        raise HTTPException(status_code=404, detail="Employee does not exist")
    
    if not employee_to_update.status:
        raise HTTPException(status_code=404, detail="Employee is already deativated")

    if employee_to_update.company_id != company.company_id:
        raise HTTPException(status_code=403, detail="Method not allowed for this employee")
    
    employee_to_update.status = False
    session.commit()
    session.refresh(employee_to_update)
    return {"Mesasage" : "Employee has been Deactivated", "Employee" : employee_to_update.employee_id, "Status": "Deactivated"}

def display_all_employee_in_db(page, page_size, department, team, current_admin, session):
    
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    
    query = select(Employee).where(Employee.company_id == company.id, Employee.status == True)

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

def update_roles_in_db(employee_id, lst, current_admin, session):
    if employee_id == "string":
        raise HTTPException(status_code=400, detail="Enter employee_id")

    # Get company of admin
    company = session.exec(
        select(Company).where(Company.company_name == current_admin.company_name)
    ).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")

    # Check for existing employee
    employee = session.exec(
        select(Employee).where(Employee.employee_id == employee_id, Employee.company_id == company.company_id)
    ).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if not employee.status:
        raise HTTPException(status_code=404, detail="Employee is deactivated")

    # --- Delete existing role links and roles ---
    existing_links = session.exec(
        select(EmployeeAdditionalRoleLink).where(EmployeeAdditionalRoleLink.employee_id == employee_id)
    ).all()

    for link in existing_links:
        # Delete linked role first
        role = session.exec(select(AdditionalRole).where(AdditionalRole.id == link.role_id)).first()
        if role:
            session.delete(role)
        # Delete link
        session.delete(link)

    session.commit()

    # --- Add new roles and links ---
    for role_data in lst:
        new_role = AdditionalRole(
            role_name=role_data.role_name,
            role_description=role_data.role_description
        )
        session.add(new_role)
        session.commit()  # commit to get new_role.id
        session.refresh(new_role)

        new_link = EmployeeAdditionalRoleLink(
            employee_id=employee_id,
            role_id=new_role.id
        )
        session.add(new_link)

    session.commit()

    return {"Message": "Roles Updated", "Roles": lst}
