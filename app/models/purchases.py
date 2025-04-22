from pydantic import BaseModel
from typing import List
from uuid import UUID
from typing import Optional

class PurchaseItemIn(BaseModel):
    name: str
    ordered_price: int
    amount: int
    save_item: bool = True  # previously was at the top level

class CostBreakdown(BaseModel):
    name: str
    amount: int
    
class DiscountBreakdown(BaseModel):
    name: str
    amount: int

class PurchaseIn(BaseModel):
    items: List[PurchaseItemIn]
    additional_cost: Optional[List[CostBreakdown]] = []
    discount: Optional[List[DiscountBreakdown]] = []
    final_total: int

class PurchaseItemOut(BaseModel):
    name: str
    amount: int
    ordered_price: int
    original_price: int
    final_price: int

class PurchaseOut(BaseModel):
    id: UUID
    items: List[PurchaseItemOut]
    final_total: int
    items_subtotal: Optional[int] = 0
    additional_cost_total: Optional[int] = 0
    discount_total: Optional[int] = 0

