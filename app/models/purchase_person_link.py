from typing import List
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID

import app.models.persons
import app.models.purchases

class PurchasePersonLink(SQLModel, table=True):
    purchase_item_id: UUID = Field(foreign_key="purchaseitem.id", primary_key=True)
    person_id: UUID = Field(foreign_key="person.id", primary_key=True)

    # Relationships using string references to avoid circular import
    purchase_item: "app.models.purchases.PurchaseItem" = Relationship(back_populates="persons_link")
    person: "app.models.persons.Person" = Relationship(back_populates="purchases")