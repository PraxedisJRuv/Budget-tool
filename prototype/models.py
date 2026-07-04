from datetime import datetime
from typing import Optional, Literal, List
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON
from pydantic import BaseModel

"""

"""
class Products_Table(SQLModel, table =True):
    __tablename__="products"
    id: int=Field(primary_key=True)
    name: str
    cost: float
    Quantity: Optional[int]=Field(default=None)
    ID_product: int=Field(foreign_key="product.id")
    ID_buy: int=Field(foreign_key="buys.id")
    ID_expense: int=Field(foreign_key="expense.id")
    

class Product_Table(SQLModel, table=True):
    __tablename__="product"
    id: Optional[int]= Field(default=None, primary_key=True)
    name:str

class Buys_Table(SQLModel, table=True):
    __tablename__="buys"
    id: Optional[int]=Field(default=None, primary_key=True)
    date: str=Field(default_factory=lambda: datetime.now().isoformat())
    cost: Optional[float] =Field(default=None)
    local: Optional[str] = Field(default=None)
    business_type: Optional[str]= Field(default=None)
    amount_products_type: int
    ID_expense: int=Field(foreign_key="expense.id")
    
class Expense_Table(SQLModel, table=True):
    __tablename__="expense"
    id: Optional[int]=Field(default=None, primary_key=True)
    date: str=Field(default_factory=lambda: datetime.now().isoformat())
    amount: float
    concept: str 
    description: Optional[str]=Field(default=None)
class Income_Table(SQLModel, table=True):
    __tablename__="income"
    id: Optional[int]=Field(default=None, primary_key=True)
    date: str=Field(default_factory=lambda: datetime.now().isoformat())
    amount: float
    concept: str
    description: Optional[str]=Field(default=None)
    
class Debt_Table(SQLModel, table=True):
    id: Optional[int]=Field(default=None, primary_key=True)
    date: str=Field(default_factory=lambda: datetime.now().isoformat())
    amount: float
    borrower: str
    borrowed: str
    interest: Optional[float]=Field(default=None)