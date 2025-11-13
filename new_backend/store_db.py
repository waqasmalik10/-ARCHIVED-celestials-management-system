from fastapi import HTTPException
from sqlmodel import select
from models import StoreBase, Store

def create_newstore_in_db(store, session, currentadmin):
    existing = select(Store).where(Store.unique_identifier == store.unique_identifier)
    if existing:
        raise HTTPException(status_code=400, detail="Store already exists")
    store = Store.model_validate(store)
    store.company_id = currentadmin.id
    session.add(store)
    session.commit()
    session.refresh(store)
    return