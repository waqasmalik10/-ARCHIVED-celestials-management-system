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

def get_all_stores_in_db(page, page_size, session, currentadmin):
    query = select(Store).where(Store.company_id == currentadmin.id)
    all_stores = session.exec(query).all()
    total_count = len(all_stores)

    offset = (page - 1) * page_size
    paginated_stores = all_stores[offset:offset + page_size]

    if not paginated_stores:
        raise HTTPException(status_code=404, detail="No stores found for this query")

    return {
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": (total_count + page_size - 1) // page_size,
        "stores": paginated_stores
    }

def get_store_by_id_in_db(store_id, session, currentadmin):
    store = session.exec(select(Store).where(Store.unique_identifier == store_id)).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    if store.company_id != currentadmin.id:
        raise HTTPException(status_code=403, detail="Method not allowed for this store")
    return store