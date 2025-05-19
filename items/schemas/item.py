from pydantic import BaseModel, ConfigDict

class ItemCreate(BaseModel):
    name: str
    description: str
    owner_id: int

class ItemOut(BaseModel):
    item_id: int
    name: str
    description: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

