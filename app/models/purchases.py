from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from app.models.purchase_person_link import PurchasePersonLink

# --- TABLE MODELS ---

class Purchase(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    final_total: int = Field(index=True)  # ✅ if you want to search/sort by this
    items_subtotal: Optional[int] = Field(default=0, index=True)  # ✅
    additional_cost_total: Optional[int] = Field(default=0, index=True)  # ✅
    discount_total: Optional[int] = Field(default=0, index=True)  # ✅

    items: List["PurchaseItem"] = Relationship(back_populates="purchase")
    additional_costs: List["AdditionalCost"] = Relationship(back_populates="purchase")
    discounts: List["Discount"] = Relationship(back_populates="purchase")

class PurchaseItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True)  # ✅ add index
    amount: int = Field(index=True)  # ✅ add index
    ordered_price: int
    original_price: int
    final_price: int
    purchase_id: UUID = Field(foreign_key="purchase.id")

    purchase: Optional["Purchase"] = Relationship(back_populates="items")
    persons_link: List["PurchasePersonLink"] = Relationship(back_populates="purchase_item")

# --- REQUEST & RESPONSE MODELS ---

class PersonInItem(BaseModel):
    name: str
    photo_url: Optional[str] = None
    save_person: bool = False

class AdditionalCost(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True)  # ✅ index for name
    amount: int = Field(index=True)  # ✅ index for amount
    purchase_id: UUID = Field(foreign_key="purchase.id")

    purchase: Optional[Purchase] = Relationship(back_populates="additional_costs")

class AdditionalCostOut(BaseModel):
    name: str
    amount: int

class Discount(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True)  # ✅
    amount: int = Field(index=True)  # ✅
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
    persons: Optional[List[PersonInItem]] = []  # ✅ Correct: list of persons assigned to this item

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