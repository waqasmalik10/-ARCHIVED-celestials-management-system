from sqlmodel import Session, select
from models import AdditionalRole
from admin_db import engine
def seed_roles(session: Session):
    default_roles = [
        {"role_name": "hr", "role_description": "salary_management"},
        {"role_name": "teamlead", "role_description": "operations_manager"}
    ]

    for role_data in default_roles:
        existing = session.exec(select(AdditionalRole).where(AdditionalRole.role_name == role_data["role_name"])).first()
        if not existing:
            session.add(AdditionalRole(**role_data))

    session.commit()
    print("Default roles seeded successfully.")

if __name__ == "__main__":
    with Session(engine) as session:
        seed_roles(session)