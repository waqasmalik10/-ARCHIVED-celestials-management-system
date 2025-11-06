from fastapi import Request
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import db
from models import AdminBase, AdminResponse, Employee, AdditionalRoleBase, AdditionalRole
import auth

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


router_login = APIRouter(prefix="/admin")


@router_login.post("/login")
def company_login(form_data: OAuth2PasswordRequestForm = Depends(),
                  session=Depends(db.get_session),
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


app.include_router(router_login)


@app.post("/register_admin")
def register_admin(admin: AdminBase, session: Session = Depends(db.get_session)):
    db.create_admin_in_db(admin, session)
    return 'Admin Created successfully'


@app.get("/company_profile")
def get_company_profile(admin: AdminBase = Depends(auth.get_current_user)):
    print(admin.company_name)
    return {"Comapany Name": admin.company_name, "Website": admin.website, "Address": admin.address, "Phone No.": admin.phone, "Email" : admin.email}


@app.put("/update_company_profile")
def update_company_profile(admin: AdminResponse,
                           current_admin: AdminBase = Depends(auth.get_current_user), session: Session = Depends(db.get_session)):
    return db.update_company_profile_in_db(admin,  current_admin, session)


@app.patch("/update_password")
def update_password(old:str, new: str, current_admin: AdminBase = Depends(auth.get_current_user),
                    session: Session = Depends(db.get_session)):
    return db.update_password_in_db(old, new, current_admin, session)


@app.post("/create_employee")
def register_new_employee(employee: Employee, lst: list[AdditionalRoleBase], current_admin: AdminBase = Depends(auth.get_current_user),
                    session: Session = Depends(db.get_session)):
    return db.register_new_employee_in_db(employee, lst, current_admin, session)

@app.patch("/update_employee_details")
def update_employee_details(employee: Employee, lst: list[AdditionalRoleBase], current_admin: AdminBase = Depends(auth.get_current_user),
                    session: Session = Depends(db.get_session)):
    return db.update_employee_details_in_db(employee, lst, current_admin, session)