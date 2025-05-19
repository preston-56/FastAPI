from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Order
from orders import schemas

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order in the database from the provided order data.
    """
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return schemas.OrderOut.model_validate(db_order)

@router.get("/", response_model=list[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    """
    Retrieve a list of all orders from the database.
    """
    orders = db.query(Order).all()
    return [schemas.OrderOut.model_validate(order) for order in orders]

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific order by its ID.
    Raises 404 if the order is not found.
    """
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return schemas.OrderOut.model_validate(order)
