from datetime import datetime
from typing import Optional, Literal, List
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON
from pydantic import BaseModel, field_validator


def normalize_date_value(value):
    """Return a consistent YYYY-MM-DD string even when the incoming value contains time data."""
    if value is None:
        return datetime.now().date().isoformat()

    if isinstance(value, datetime):
        return value.date().isoformat()

    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return datetime.now().date().isoformat()

        iso_candidate = raw.replace("Z", "+00:00")
        if "T" in iso_candidate or " " in iso_candidate:
            try:
                return datetime.fromisoformat(iso_candidate).date().isoformat()
            except ValueError:
                raw = raw.split(" ")[0].split("T")[0]

        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(raw[:10] if len(raw) >= 10 else raw, fmt).date().isoformat()
            except ValueError:
                continue

        return raw[:10]

    return str(value)


"""
Products
"""
class Items_Base(SQLModel):
    name: str
    cost: float
    Quantity: Optional[int]=Field(default=None)
class Items_Table(Items_Base, table =True):
    __tablename__="products"
    id: int=Field(primary_key=True)
    ID_product: int=Field(foreign_key="product.id")
    ID_buy: int=Field(foreign_key="buys.id")
    ID_expense: int=Field(foreign_key="expense.id")
    
class Items_Record(Items_Base):
    pass

class Items_Public(Items_Base):
    id: int
    ID_product: int
    ID_buy: int
    ID_expense: int
    
class Items_List(BaseModel):
    items: List[Items_Public]
    total: int
    offset: int
    limit: int
    
class Items_Update(SQLModel):
    name: str | None = None
    cost: float | None = None
    Quantity: int | None = None
    ID_product: int | None = None
    ID_buy: int | None = None
    ID_expense: int | None = None


"""
Product
"""
class Product_Base(SQLModel):
    name: str
class Product_Table(Product_Base, table=True):
    __tablename__="product"
    id: Optional[int]= Field(default=None, primary_key=True)

class Product_Record(Product_Base):
    pass

class Product_Public(Product_Base):
    id: int
    
class Product_List(BaseModel):
    items: List[Product_Public]
    total: int
    offset: int
    limit: int
    
class Product_Update(SQLModel):
    name:str

"""
Buys
"""
class Buy_Base(SQLModel):
    date: str = Field(default_factory=lambda: datetime.now().date().isoformat())
    cost: Optional[float] = Field(default=None)
    local: Optional[str] = Field(default=None, max_length=25)
    business_type: Optional[str] = Field(default=None)
    amount_products_type: int

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value):
        return normalize_date_value(value)


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
class Expense_Base(SQLModel):
    date: str = Field(default_factory=lambda: datetime.now().date().isoformat())
    amount: float
    concept: str
    description: Optional[str] = Field(default=None)

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value):
        return normalize_date_value(value)


class Expense_Table(Expense_Base, table=True):
    __tablename__="expense"
    id: Optional[int]=Field(default=None, primary_key=True)

class Expense_Record(Expense_Base):
    pass

class Expense_Public(Expense_Base):
    id: int

class Expense_List(BaseModel):
    items: List[Expense_Public]
    total: int
    offset: int
    limit: int

class Expense_Update(SQLModel):
    id: int | None=None
    date: str | None=None
    amount: float | None=None
    concept: str | None=None
    description: str | None=None
    
"""
Income
"""

class Income_Base(SQLModel):
    date: str = Field(default_factory=lambda: datetime.now().date().isoformat())
    amount: float
    concept: str
    description: Optional[str] = Field(default=None)

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value):
        return normalize_date_value(value)


class Income_Table(Income_Base, table=True):
    __tablename__="income"
    id: Optional[int]=Field(default=None, primary_key=True)
    
class Income_Record(Income_Base):
    pass

class Income_Public(Income_Base):
    id: int
        
class Income_List(BaseModel):
    items: List[Income_Public]
    total: int
    offset: int
    limit: int
    
class Income_Update(SQLModel):
    id: int | None=None
    date: str | None=None
    amount: float | None=None
    concept: str | None=None
    description: str | None=None
"""
Debt
"""
class Debt_Base(SQLModel):
    date: str = Field(default_factory=lambda: datetime.now().date().isoformat())
    amount: float
    borrower: str
    borrowed: str
    interest: Optional[float] = Field(default=None)

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value):
        return normalize_date_value(value)


class Debt_Table(Debt_Base, table=True):
    __tablename__="debt"
    id: Optional[int]=Field(default=None, primary_key=True)

class Debt_Record(Debt_Base):
    pass

class Debt_Public(Debt_Base):
    id: int

class Debt_List(BaseModel):
    items: List[Debt_Public]
    total: int
    offset: int
    limit: int
    
class Debt_Update(SQLModel):
    date: str | None=None
    amount: float | None=None
    borrower: str | None=None
    borrowed: str | None=None
    interest: float | None=None

"""
Composite Models for Atomic Transactions
"""
class ItemInBuy(SQLModel):
    """Item/product with quantity being purchased in a buy"""
    product_name: str
    cost: float
    Quantity: int

class BuyWithItemsRecord(SQLModel):
    """Complete buy transaction: buy + items + expense (ATOMIC)"""
    # Buy data
    date: str = Field(default_factory=lambda: datetime.now().date().isoformat())
    local: Optional[str] = Field(default=None, max_length=25)
    business_type: Optional[str] = None
    # Items being bought
    items: List[ItemInBuy]
    # Expense details
    expense_concept: str
    expense_description: Optional[str] = None

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value):
        return normalize_date_value(value)

class BuyWithItemsResponse(SQLModel):
    """Response showing all created entities from atomic buy"""
    buy: Buy_Public
    expense: Expense_Public
    items: List[Items_Public]