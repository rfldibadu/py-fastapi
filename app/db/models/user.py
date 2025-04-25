# app/models/user.py
from typing import Optional
from sqlmodel import UUID, SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default=None, primary_key=True)
    name: str
    email: str
