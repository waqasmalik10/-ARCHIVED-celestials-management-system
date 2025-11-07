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