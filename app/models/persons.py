from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Optional, List

import app.models.purchase_person_link  # <<< NOT from import, but import module

class Person(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    photo_url: Optional[str] = None

    purchases: List["app.models.purchase_person_link.PurchasePersonLink"] = Relationship(
    back_populates="person",
    sa_relationship_kwargs={"cascade": "all, delete-orphan"}
)

# Input model for creating person (API / internal use)
class PersonIn(SQLModel):
    name: str
    photo_url: Optional[str] = None
    save_person: bool = True

# Output model if needed
class PersonOut(SQLModel):
    id: UUID
    name: str
    photo_url: Optional[str] = None
