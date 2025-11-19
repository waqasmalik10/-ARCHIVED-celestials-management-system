from fastapi import HTTPException
from sqlmodel import select
from models import Company, Store, ItemCategory, StoreItems

def create_newstore_in_db(store, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    existing = session.exec(select(Store).where(Store.unique_identifier == store.unique_identifier,
                                                Store.company_id == company.company_id)).first()
    if existing:
        raise HTTPException(status_code=409, detail="Store already exists")
    store = Store.model_validate(store)
    store.company_id = company.company_id
    session.add(store)
    session.commit()
    session.refresh(store)
    return store

def update_store_details_in_db(store, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    existing = session.exec(select(Store).where(Store.unique_identifier == store.unique_identifier,
                                                Store.company_id == company.company_id)).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Store does not exists")
    if existing.company_id != company.company_id:
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

def get_all_stores_in_db(page, page_size, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    all_stores = session.exec(select(Store).where(Store.company_id == company.company_id)).all()
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

def get_store_by_id_in_db(store_id, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    store = session.exec(select(Store).where(Store.unique_identifier == store_id,
                                             Store.company_id == company.company_id)).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

def Create_new_Category_for_store_items_in_db(item_category, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    if item_category.name == 'string':
        raise HTTPException(status_code=400, detail="Enter Name of Category")
    if item_category.store_id == 0:
        raise HTTPException(status_code=400, detail="Enter ID of the store")
    store = session.exec(select(Store).where(Store.id == item_category.store_id)).first()
    if store.company_id != company.company_id:
        raise HTTPException(status_code=404, detail='Store Does not exists')
    existing = session.exec(select(ItemCategory).where(ItemCategory.name == item_category.name,
                                                       ItemCategory.company_id == company.company_id,
                                                       ItemCategory.store_id == item_category.store_id)).first()
    if existing:
        raise HTTPException(status_code=409, detail='Item Category already exists')
    item_category = ItemCategory.model_validate(item_category)
    item_category.company_id = company.company_id
    session.add(item_category)
    session.commit()
    session.refresh(item_category)
    return item_category


def Update_details_of_Category_for_store_items_in_db(item_category_id, item_category, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    existing = session.exec(select(ItemCategory).where(ItemCategory.id == item_category_id)).first()
    if not existing:
        raise HTTPException(status_code=404, detail='Item Category does not exists')
    if existing.company_id != company.company_id:
        raise HTTPException(status_code=404, detail='Item Category does not exists')
    if item_category.name != 'string':
        existing.name = item_category.name 
    if item_category.description != 'string':
        existing.description = item_category.description 
    if item_category.store_id != 'string':
        existing.store_id = item_category.store_id
    session.commit()
    session.refresh(existing) 
    return existing

def get_category_by_id_in_db(item_category_id, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    existing = session.exec(select(ItemCategory).where(ItemCategory.id == item_category_id,
                                                       ItemCategory.company_id == company.company_id)).first()
    if not existing:
        raise HTTPException(status_code=409, detail='Item Category does not exists')
    return existing

def get_all_categories_id_in_db(page, page_size, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    all_categories = session.exec(select(ItemCategory).where(ItemCategory.company_id == company.company_id)).all()
    total = len(all_categories)
    offset = (page - 1) * page_size
    paginated_categories = all_categories[offset:offset + page_size]

    if not paginated_categories:
        raise HTTPException(status_code=404, detail="No stores found for this query")

    return {
        "page": page,
        "page_size": page_size,
        "total_count": total,
        "total_pages": (total + page_size - 1) // page_size,
        "categories": paginated_categories.store_id
    }

def Create_store_items_in_db(item, session, current_admin):
    company = session.exec(select(Company).where(Company.company_name == current_admin.company_name)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company Doesn't Found for Admin")
    if item.name == 'string':
        raise HTTPException(status_code=400, detail="Enter Name of Item")
    if item.quantity == 0:
        raise HTTPException(status_code=400, detail="Enter quantity of Item")
    if item.category_id == 0:
        raise HTTPException(status_code=400, detail="Enter category id of Item")
    if item.store_id == 0:
        raise HTTPException(status_code=400, detail="Enter store id of Item")
    store = session.exec(select(Store).where(Store.id == item.store_id,
                                                Store.company_id == company.company_id)).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store does not exists")
    category = session.exec(select(ItemCategory).where(ItemCategory.id == item.category_id,
                                                        ItemCategory.store_id == item.store_id,
                                                        ItemCategory.company_id == company.company_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="category does not exists in given store")
    existing = session.exec(select(StoreItems).where(StoreItems.name == item.name,
                                                        StoreItems.store_id == item.store_id,
                                                        StoreItems.category_id == item.category_id,
                                                        )).first()
    if existing:
        raise HTTPException(status_code=409, detail='Item already exists in store')
    item = StoreItems.model_validate(item)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item