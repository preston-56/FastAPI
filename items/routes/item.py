from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Item
from items import schemas

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=schemas.ItemOut)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)) -> schemas.ItemOut:
    """
    Create a new item in the database.
    """
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return schemas.ItemOut.model_validate(db_item)

@router.get("/", response_model=list[schemas.ItemOut])
def list_items(db: Session = Depends(get_db)) -> list[schemas.ItemOut]:
    """
    Retrieve a list of all items.
    """
    items = db.query(Item).all()
    return [schemas.ItemOut.model_validate(i) for i in items]
@router.get("/{item_id}", response_model=schemas.ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)) -> schemas.ItemOut:
    """
    Retrieve a single item by its ID.
    Raises 404 if the item is not found.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return schemas.ItemOut.model_validate(item)