from datetime import datetime, timezone, date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, select, Session


class AdminResponse(SQLModel):
    company_name: str = Field(..., min_length=1)
    website: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)


class AdminBase(AdminResponse):
    password: str = Field(..., min_length=1)


class Admin(AdminBase, table=True):
    __tablename__ = "admin"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)


# --- Additional Roles Table ---
class AdditionalRoleBase(SQLModel):
    role_name: str = Field(..., min_length=1)
    role_description: Optional[str] = None


class AdditionalRole(AdditionalRoleBase, table=True):
    __tablename__ = "additional_roles"

    id: Optional[int] = Field(default=None, primary_key=True, unique=True, index=True)
    employees: List["EmployeeAdditionalRoleLink"] = Relationship(back_populates="role")


# --- Link table for Many-to-Many relation ---
class EmployeeAdditionalRoleLink(SQLModel, table=True):
    __tablename__ = "employee_additional_roles"

    # Use employee_id as foreign key to employee table (PK)
    employee_id: str = Field(
        foreign_key="employee.employee_id", primary_key=True
    )
    role_id: int = Field(
        foreign_key="additional_roles.id", primary_key=True
    )

    # Relationships
    employee: Optional["Employee"] = Relationship(back_populates="additional_roles")
    role: Optional["AdditionalRole"] = Relationship(back_populates="employees")
    
# --- Employee Table ---
class EmployeeIncrementBase(SQLModel):
    employee_id: str = Field(foreign_key="employee.id", nullable=False)
    increment_amount: float
    effective_date: date
    notes: Optional[str] = Field(default=None)


class EmployeeIncrement(EmployeeIncrementBase, table=True):
    __tablename__ = "employee_increment_history"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship back to Employee (ensure Employee model defines increments)
    employee: Optional["Employee"] = Relationship(back_populates="increments")

class EmployeeBase(SQLModel):
    employee_id: str = Field(...,unique=True)
    name: str
    bank_name: str
    bank_account_title: str
    bank_branch_code: str
    bank_account_number: str
    bank_iban_number: str
    initial_base_salary: float
    current_base_salary: float
    date_of_joining: date
    fulltime_joining_date: Optional[date] = None
    last_increment_date: Optional[date] = None
    increment_amount: float = 0.0
    department: str
    team: str
    home_address: str
    email: str
    password: str
    designation: str
    cnic: str
    date_of_birth: date
    actual_date_of_birth: Optional[date] = None
    hobbies: Optional[str] = None
    vehicle_registration_number: Optional[str] = None
    company_id: int = Field(foreign_key="admin.id")
    
    
class Employee(EmployeeBase, table=True):
    __tablename__ = "employee"

    # 🔑 employee_id is now the PRIMARY KEY
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    status: bool = Field(default=True)

    # ✅ Relationship: optional roles, many-to-many
    additional_roles: List[EmployeeAdditionalRoleLink] = Relationship(back_populates="employee")
    increments: list[EmployeeIncrement] = Relationship(back_populates="employee")
