from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class ItemBase(SQLModel):
    name: str
    price: int
    store_name: Optional[str] = None

class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class ItemCreate(ItemBase):
    pass

class ItemIn(ItemCreate):
    pass

class ItemRead(ItemBase):
    id: UUID
