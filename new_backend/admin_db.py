from sqlmodel import create_engine, Session, select
from fastapi import HTTPException
from models import Admin, Company

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

def register_company_in_db(company, session):
    if company.company_id == 'string':
        raise HTTPException(status_code=400, detail="Enter company_id")
    if company.company_name == 'string':
        raise HTTPException(status_code=400, detail="Enter company_name")
    if company.website == 'string':
        raise HTTPException(status_code=400, detail="Enter website")
    if company.address == 'string':
        raise HTTPException(status_code=400, detail="Enter address")
    if company.phone == 'string':
        raise HTTPException(status_code=400, detail="Enter phone")
    if company.email == 'string':
        raise HTTPException(status_code=400, detail="Enter email")
    company = Company.model_validate(company)
    session.add(company)
    session.commit()
    session.refresh(company)
    return company

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
        raise HTTPException(status_code=409, detail="User already exists")

    db_admin = Admin.model_validate(admin)
    session.add(db_admin)
    session.commit()
    session.refresh(db_admin)
    return {
        "message": "Admin created successfully",
        "admin": db_admin
    }


def update_company_profile_in_db(company, session, current_admin):
    existing = session.exec(
        select(Company).where(Company.company_id == company.company_id)).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Company Does not exists")
    if existing.company_name != current_admin.company_name:
        raise HTTPException(status_code=403, detail="Method not allowed for this Company")
    if company.company_name != 'string':
        existing.company_name = company.company_name
    if company.website != 'string':
        existing.website = company.website
    if company.address != 'string':
        existing.address = company.address
    if company.phone != 'string':
        existing.phone = company.phone
    if company.email != 'string':
        existing.email = company.email
    
    session.commit()
    session.refresh(existing)
    return existing


def update_password_in_db(old, new, current_admin, session):
    if old == current_admin.password:
        current_admin.password = new
        session.commit()
        session.refresh(current_admin)
        return "Password Update"
    else:
        raise HTTPException(status_code=403, detail="Provided password is wrong")