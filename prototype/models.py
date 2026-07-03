import datetime
from typing import Optional, Literal, List
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON
from pydantic import BaseModel

"""

"""
class Products_Table(SQLModel):
    id: int
    name: str
    cost: float
    Quantity: Optional[int]=Field(default=None)
    ID_product: int=Field(foreign_key="product.id")
    ID_session: int=Field(foreign_key="session.id")
    ID_expense: int=Field(foreign_key="expense.id")
    
    