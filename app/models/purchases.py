from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

# --- TABLE MODELS ---

class Purchase(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    final_total: int
    items_subtotal: Optional[int] = 0
    additional_cost_total: Optional[int] = 0
    discount_total: Optional[int] = 0

    items: list["PurchaseItem"] = Relationship(back_populates="purchase")
    additional_costs: list["AdditionalCost"] = Relationship(back_populates="purchase")
    discounts: list["Discount"] = Relationship(back_populates="purchase")

class PurchaseItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    amount: int
    ordered_price: int
    original_price: int
    final_price: int
    purchase_id: UUID = Field(foreign_key="purchase.id")

    purchase: Optional[Purchase] = Relationship(back_populates="items")

class AdditionalCost(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    amount: int
    purchase_id: UUID = Field(foreign_key="purchase.id")

    purchase: Optional[Purchase] = Relationship(back_populates="additional_costs")

class AdditionalCostOut(BaseModel):
    name: str
    amount: int

class Discount(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    amount: int
    purchase_id: UUID = Field(foreign_key="purchase.id")

    purchase: Optional[Purchase] = Relationship(back_populates="discounts")

class DiscountOut(BaseModel):
    name: str
    amount: int

class PurchaseItemBase(BaseModel):
    name: str
    amount: int
    ordered_price: int
    save_item: bool

class PurchaseItemOut(BaseModel):
    name: str
    amount: int
    ordered_price: int
    original_price: int
    final_price: int

class CostBase(BaseModel):
    name: str
    amount: int

class PurchaseIn(BaseModel):
    items: List[PurchaseItemBase]
    additional_cost: Optional[List[CostBase]] = None
    discount: Optional[List[CostBase]] = None
    final_total: int

class PurchaseOut(BaseModel):
    id: UUID
    items: List[PurchaseItemOut]
    items_subtotal: Optional[int] = 0
    discounts: List[DiscountOut]
    discount_total: Optional[int] = 0
    additional_costs: List[AdditionalCostOut]
    additional_cost_total: Optional[int] = 0
    final_total: int
    

    
