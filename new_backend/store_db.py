from fastapi import HTTPException
from sqlmodel import select
from models import StoreBase, Store

def create_newstore_in_db(store, session, currentadmin):
    existing = session.exec(select(Store).where(Store.unique_identifier == store.unique_identifier)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Store already exists")
    store = Store.model_validate(store)
    store.company_id = currentadmin.id
    session.add(store)
    session.commit()
    session.refresh(store)
    return store

def update_store_details_in_db(store, session, currentadmin):
    existing = session.exec(select(Store).where(Store.unique_identifier == store.unique_identifier)).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Store does not exists")
    if existing.company_id != currentadmin.id:
        raise HTTPException(status_code=403, detail="Method not allowed for this store")
    if store.name != 'string':
        existing.name = store.name
    if store.unique_identifier != 'string':
        existing.unique_identifier = store.unique_identifier
    if store.description != 'string':
        existing.description = store.description
    session.commit()
    session.refresh(existing)
    return existing