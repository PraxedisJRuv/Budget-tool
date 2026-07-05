from datetime import datetime
from typing import Optional, Literal, List
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON
from pydantic import BaseModel

"""
Products
"""
class Products_Base(SQLModel):
    name: str
    cost: float
    Quantity: Optional[int]=Field(default=None)
class Products_Table(Products_Base, table =True):
    __tablename__="products"
    id: int=Field(primary_key=True)
    ID_product: int=Field(foreign_key="product.id")
    ID_buy: int=Field(foreign_key="buys.id")
    ID_expense: int=Field(foreign_key="expense.id")
    
class Products_Record(Products_Base):
    pass

class Products_Public(Products_Base):
    id: int
    ID_product: int
    ID_buy: int
    ID_expense: int
    
class Products_List(BaseModel):
    items: List[Products_Public]
    total: int
    offset: int
    limit: int
    
class Products_Update(SQLModel):
    name: str | None = None
    cost: float | None = None
    Quantity: int | None = None
    ID_product: int | None = None
    ID_buy: int | None = None
    ID_expense: int | None = None


"""
Product
"""

class Product_Table(SQLModel, table=True):
    __tablename__="product"
    id: Optional[int]= Field(default=None, primary_key=True)
    name:str

"""
Buys
"""
class Buy_Base(SQLModel):
    date: str=Field(default_factory=lambda: datetime.now().isoformat())
    cost: Optional[float] =Field(default=None)
    local: Optional[str] = Field(default=None, max_length=25)
    business_type: Optional[str]= Field(default=None)
    amount_products_type: int
class Buys_Table(Buy_Base, table=True):
    __tablename__="buys"
    id: Optional[int]=Field(default=None, primary_key=True)
    ID_expense: int=Field(foreign_key="expense.id")
    
class Buy_Record(Buy_Base):
    pass

class Buy_Public(Buy_Base):
    id: int
    ID_expense: int

class Buy_List(BaseModel):
    items: List[Buy_Public]
    total: int
    offset: int
    limit: int

class Buy_Update(SQLModel):
    date: str | None=None
    cost: float | None=None
    local: str | None=None
    business_type: str | None=None
    amount_products_type: int | None = None
    ID_expense: int | None = None

"""
Expense
"""
class Expense_Table(SQLModel, table=True):
    __tablename__="expense"
    id: Optional[int]=Field(default=None, primary_key=True)
    date: str=Field(default_factory=lambda: datetime.now().isoformat())
    amount: float
    concept: str 
    description: Optional[str]=Field(default=None)

"""
Income
"""

class Income_Table(SQLModel, table=True):
    __tablename__="income"
    id: Optional[int]=Field(default=None, primary_key=True)
    date: str=Field(default_factory=lambda: datetime.now().isoformat())
    amount: float
    concept: str
    description: Optional[str]=Field(default=None)
    
"""
Debt
"""
class Debt_Table(SQLModel, table=True):
    id: Optional[int]=Field(default=None, primary_key=True)
    date: str=Field(default_factory=lambda: datetime.now().isoformat())
    amount: float
    borrower: str
    borrowed: str
    interest: Optional[float]=Field(default=None)
    
    """
    
    """