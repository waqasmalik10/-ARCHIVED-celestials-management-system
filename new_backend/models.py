from datetime import date
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
    employee_id: int = Field(foreign_key="employee.id", nullable=False)
    increment_amount: float
    effective_date: date
    notes: Optional[str] = Field(default=None)


class EmployeeIncrement(EmployeeIncrementBase, table=True):
    __tablename__ = "employee_increment_history"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship back to Employee (ensure Employee model defines increments)
    employee: Optional["Employee"] = Relationship(back_populates="increments")



class EmployeeBase(SQLModel):
    employee_id: str
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


class Employee(EmployeeBase, table=True):
    __tablename__ = "employee"

    # 🔑 Primary key
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    
    # 🏢 Move company_id here
    company_id: int = Field(foreign_key="admin.id")

    # ✅ Additional fields and relationships
    status: bool = Field(default=True)
    additional_roles: List["EmployeeAdditionalRoleLink"] = Relationship(back_populates="employee")
    increments: List["EmployeeIncrement"] = Relationship(back_populates="employee")

# --- Finance Category Table ---
class FinanceCategoryBase(SQLModel):
    category_name: str = Field(..., min_length=1)
    color_code: str = Field(..., min_length=1)


class FinanceCategory(FinanceCategoryBase, table=True):
    __tablename__ = "finance_categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="admin.id")  # company creating this category

    # Relationship with Finance
    finances: List["Finance"] = Relationship(back_populates="category")


# --- Finance Table ---
class FinanceBase(SQLModel):
    date: date = Field(default_factory=date.today) # pyright: ignore[reportInvalidTypeForm]
    description: str = Field(..., min_length=1)
    amount: float = Field(..., ge=0)
    tax_deductions: float = Field(default=0.0, ge=0)
    cheque_number: Optional[str] = Field(default=None)
    category_id: int = Field(...) # input category


class Finance(FinanceBase, table=True):
    __tablename__ = "finance"

    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="admin.id")  # company creating this record
    added_by: int = Field(foreign_key="admin.id")  # keep this

    # Relationships
    category: Optional["FinanceCategory"] = Relationship(back_populates="finances")
    company: Optional["Admin"] = Relationship(back_populates="finances")
    added_by_admin: Optional["Admin"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Finance.added_by"}
    )