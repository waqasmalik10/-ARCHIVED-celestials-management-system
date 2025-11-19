from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, date
import admin_db, auth, employee_db, increment_db, finance_db, store_db
from models import Company, AdminBase, AdminResponse, EmployeeBase, AdditionalRoleBase, EmployeeIncrementBase, FinanceBase, StoreBase, ItemCategoryBase, StoreItemsBase
from typing import Optional

app = FastAPI(title="Celestials Management System")


current_tokens = {}

@app.middleware("http")
async def auto_auth_middleware(request: Request, call_next):
    client_ip = request.client.host
    if request.url.path.endswith("/admin/login") and request.method == "POST":
        response = await call_next(request)
        try:
            data = await response.body()
        except Exception:
            data = None
        return response
    token = current_tokens.get(client_ip)
    if token:
        request.headers.__dict__["_list"].append(
            (b"authorization", f"Bearer {token}".encode())
        )

    response = await call_next(request)
    return response

@app.post("/register_company", status_code=201)
def register_company(company: Company, session=Depends(admin_db.get_session)):
    return admin_db.register_company_in_db(company, session)

router_login = APIRouter(prefix="/admin")

@router_login.post("/login")
def company_login(form_data: OAuth2PasswordRequestForm = Depends(),session=Depends(admin_db.get_session),
                    request: Request = None):
    admin = auth.authenticate_admin(session, form_data.username, form_data.password)
    if not admin or admin.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = auth.create_access_token(data={"user_id": admin.id}, expires_delta=access_token_expires)

    # store token for that client
    client_ip = request.client.host
    current_tokens[client_ip] = token

    return {"access_token": token, "token_type": "bearer"}



@app.post("/register_admin", status_code=201)
def register_admin(admin: AdminBase, session: Session = Depends(admin_db.get_session)):
    admin_db.create_admin_in_db(admin, session)
    return 'Admin Created successfully'


@router_login.get("/company_profile")
def get_company_profile(admin: AdminBase = Depends(auth.get_current_user)):
    return {"Comapany Name": admin.company_name, "Website": admin.website,
            "Address": admin.address, "Phone No.": admin.phone, "Email" : admin.email}


@router_login.put("/update_company_profile")
def update_company_profile(company: Company,
                            current_admin: AdminBase = Depends(auth.get_current_user),
                            session: Session = Depends(admin_db.get_session)):
    return admin_db.update_company_profile_in_db(company, session, current_admin)


@router_login.patch("/update_password")
def update_password(old:str, new: str, current_admin: AdminBase = Depends(auth.get_current_user),
                    session: Session = Depends(admin_db.get_session)):
    return admin_db.update_password_in_db(old, new, current_admin, session)


@router_login.post("/create_employee")
def register_new_employee(employee: EmployeeBase, lst: list[AdditionalRoleBase], current_admin: AdminBase = Depends(auth.get_current_user),
                    session: Session = Depends(admin_db.get_session)):
    return employee_db.register_new_employee_in_db(employee, lst, current_admin, session)

@router_login.patch("/update_employee_details")
def update_employee_details(employee: EmployeeBase, current_admin: AdminBase = Depends(auth.get_current_user),
                    session: Session = Depends(admin_db.get_session)):
    return employee_db.update_employee_details_in_db(employee, current_admin, session)

@router_login.patch("/deactivate_employee")
def deactivate_employee(employee_id: str, current_admin: AdminBase = Depends(auth.get_current_user), session: Session = Depends(admin_db.get_session)):
    return employee_db.deactivate_employee_in_db(employee_id, current_admin, session)

@router_login.get("/display all employees")
def display_all_employee(page: int = 1, page_size: int = 10, department: Optional[str] = None, team: Optional[str] = None,
                            current_admin: AdminBase = Depends(auth.get_current_user), session: Session = Depends(admin_db.get_session)):
    return employee_db.display_all_employee_in_db(page, page_size, department, team, current_admin, session)

@router_login.put("/Update Roles")
def update_roles(employee_id: str, lst: list[AdditionalRoleBase], current_admin: AdminBase = Depends(auth.get_current_user),
                    session: Session = Depends(admin_db.get_session)):
    return employee_db.update_roles_in_db(employee_id, lst, current_admin, session)

@router_login.post("/create_increment")
def create_increment_in_db(new_increment: EmployeeIncrementBase, session: Session = Depends(admin_db.get_session), 
                            current_admin: AdminBase = Depends(auth.get_current_user)):
    return increment_db.create_increment_in_db(new_increment, session, current_admin)

@router_login.get("/get_increments")
def get_increment_by_id(employee_id: str, session: Session = Depends(admin_db.get_session),
                    current_admin: AdminBase = Depends(auth.get_current_user)):
    return increment_db.get_increment_by_id_in_db(employee_id, session, current_admin)

@router_login.patch("/update_increment")
def update_increment(new_increment: EmployeeIncrementBase, session: Session = Depends(admin_db.get_session),
                        current_admin: AdminBase = Depends(auth.get_current_user)):
    return increment_db.update_increment_in_db(new_increment, session, current_admin)

@router_login.put("/delete_increment")
def delete_increment(employee_id: str, session: Session = Depends(admin_db.get_session),
                        current_admin: AdminBase = Depends(auth.get_current_user)):
    return increment_db.delete_increment_in_db(employee_id, session, current_admin)

finance_router = APIRouter(prefix="/finance")

@finance_router.post("/create_finance_record")
def create_finance(finance: FinanceBase, session: Session = Depends(admin_db.get_session),
                        current_admin: AdminBase = Depends(auth.get_current_user)):
    return finance_db.create_finance_in_db(finance, session, current_admin)

@finance_router.patch("/edit_finance_record")
def edit_finance_record(finance: FinanceBase, session: Session = Depends(admin_db.get_session),
                        current_admin: AdminBase = Depends(auth.get_current_user)):
    return finance_db.edit_finance_record_in_db(finance, session, current_admin)

@finance_router.delete("/delete_finance_record")
def delete_finance_record(cheque_no: str, session: Session = Depends(admin_db.get_session),
                        current_admin: AdminBase = Depends(auth.get_current_user)):
    return finance_db.delete_finance_record_in_db(cheque_no, session, current_admin)

@finance_router.get("/get_finance_records")
def get_finance_records(page: int = 1, page_size: int = 10, start_date: Optional[date] = None,
                        end_date: Optional[date] = None, category_id: Optional[int] = None,
                        session: Session = Depends(admin_db.get_session), current_admin: AdminBase = Depends(auth.get_current_user)):
    return finance_db.get_finance_records_in_db(page, page_size, start_date, end_date, category_id, session, current_admin)

store_router = APIRouter(prefix='/store')

@store_router.post("/newstore", status_code=201)
def create_newstore(store: StoreBase, session: Session = Depends(admin_db.get_session),
                    current_admin: AdminBase = Depends(auth.get_current_user)):
    return store_db.create_newstore_in_db(store, session, current_admin)

@store_router.patch("/update_store")
def update_store_details(store: StoreBase, session: Session = Depends(admin_db.get_session),
                        current_admin: AdminBase = Depends(auth.get_current_user)):
    return store_db.update_store_details_in_db(store, session, current_admin)

@store_router.get("/get_all_stores")
def get_all_stores(page: int, page_size: int, session: Session = Depends(admin_db.get_session),
                    current_admin: AdminBase = Depends(auth.get_current_user)):
    return store_db.get_all_stores_in_db(page, page_size, session, current_admin)

@store_router.get("/get_store_by_id")
def get_store_by_id(store_id: str, session: Session = Depends(admin_db.get_session),
                    current_admin: AdminBase = Depends(auth.get_current_user)):
    return store_db.get_store_by_id_in_db(store_id, session, current_admin)

@store_router.post("/create_category_for_store_items", status_code=201)
def create_category_for_store_items(item_category: ItemCategoryBase, session: Session = Depends(admin_db.get_session),
                                    current_admin: AdminBase = Depends(auth.get_current_user)):
    return store_db.Create_new_Category_for_store_items_in_db(item_category, session, current_admin)

@store_router.patch("/Update_details_of_Category_for_store_items")
def Update_details_of_Category_for_store_items(item_category_id: int, item_category: ItemCategoryBase, session: Session = Depends(admin_db.get_session),
                                    current_admin: AdminBase = Depends(auth.get_current_user)):
    return store_db.Update_details_of_Category_for_store_items_in_db(item_category_id, item_category, session, current_admin)

@store_router.get('/get_category_by_id/{category_id}')
def get_category_by_id(item_category_id:int, session: Session = Depends(admin_db.get_session),
                                    current_admin: AdminBase = Depends(auth.get_current_user)):
    return store_db.get_category_by_id_in_db(item_category_id, session, current_admin)

@store_router.get('/get_all_categories')
def get_category_by_id(page:int, page_size:int, session: Session = Depends(admin_db.get_session),
                                    current_admin: AdminBase = Depends(auth.get_current_user)):
    return store_db.get_all_categories_id_in_db(page, page_size, session, current_admin)

@store_router.post('/Create_store_items')
def Create_store_items(item: StoreItemsBase, session: Session = Depends(admin_db.get_session),
                                    current_admin: AdminBase = Depends(auth.get_current_user)):
    return store_db.Create_store_items_in_db(item, session, current_admin)

app.include_router(router_login)
app.include_router(finance_router)
app.include_router(store_router)