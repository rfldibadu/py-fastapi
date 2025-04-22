from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ItemIn(BaseModel):
    name: str
    price: int
    store_name: Optional[str] = None

class ItemOut(ItemIn):
    id: UUID
