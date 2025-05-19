from pydantic import BaseModel, ConfigDict

class OrderCreate(BaseModel):
    user_id: int
    item_id: int

class OrderOut(BaseModel):
    order_id: int
    user_id: int
    item_id: int

    model_config = ConfigDict(from_attributes=True)
