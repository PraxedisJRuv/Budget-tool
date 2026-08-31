from fastapi import FastAPI, HTTPException, Response, Depends, Query
from utils import create_db, get_session
from models import *
app=FastAPI()

create_db()


"""
buy
"""

@app.post("/buy", response_model=Buy_Public)
def record_buy(buy: Buy_Record, session=Depends(get_session)):
    db_buy=Buys_Table.model_validate(buy)
    session.add(db_buy)
    #We should add the expense when adding a buy
    session.commit()
    session.refresh(db_buy)
    return db_buy

@app.get("/buy", response_model=Buy_List)
def get_buys(offset:int=0, limit:int=100, search: str = Query(None), session=Depends(get_session)):
    query = session.query(Buys_Table)
    if search:
        query = query.filter(Buys_Table.name.contains(search))
    buys = query.offset(offset).limit(limit).all()
    total = query.count()
    return Buy_List(items=buys, total=total, offset=offset, limit=limit)

@app.get("/buy/{buy_id}", response_model=Buy_Public)
def get_buy(buy_id:int, session=Depends(get_session)):
    buy=session.get(Buys_Table, buy_id)
    if not buy:
        raise HTTPException(status_code=404, detail="Buy not found")
    return buy

@app.put("/buy/{buy_id}", response_model=Buy_Public)
def update_buy(buy_id:int, buy: Buy_Update, session=Depends(get_session)):  
    db_buy=session.get(Buys_Table, buy_id)
    if not db_buy:
        raise HTTPException(status_code=404, detail="Buy not found")
    buy_data=buy.model_dump(exclude_unset=True)
    for key, value in buy_data.items():
        setattr(db_buy, key, value)
    session.add(db_buy)
    session.commit()
    session.refresh(db_buy)
    return db_buy

@app.delete("/buy/{buy_id}", response_model=Buy_Public)
def delete_buy(buy_id:int, session=Depends(get_session)):
    db_buy=session.get(Buys_Table, buy_id)
    if not db_buy:
        raise HTTPException(status_code=404, detail="Buy not found")
    session.delete(db_buy)
    session.commit()
    return Response(status_code=204)

"""
expense
"""

@app.post("/expense", response_model=Expense_Public)
def record_expense(expense: Expense_Record, session=Depends(get_session)):
    db_expense=Expense_Table.model_validate(expense)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense

@app.get("/expense", response_model=Expense_List)
def get_expenses(offset:int=0, limit:int=100, search: str = Query(None), session=Depends(get_session)):
    query = session.query(Expense_Table)
    if search:
        query = query.filter(Expense_Table.name.contains(search))
    expenses = query.offset(offset).limit(limit).all()
    total = query.count()
    return Expense_List(items=expenses, total=total, offset=offset, limit=limit)

@app.get("/expense/{expense_id}", response_model=Expense_Public)
def get_expense(expense_id:int, session=Depends(get_session)):
    expense=session.get(Expense_Table, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@app.put("/expense/{expense_id}", response_model=Expense_Public)
def update_expense(expense_id:int, expense: Expense_Update, session=Depends(get_session)):  
    db_expense=session.get(Expense_Table, expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense_data=expense.model_dump(exclude_unset=True)
    for key, value in expense_data.items():
        setattr(db_expense, key, value)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense

@app.delete("/expense/{expense_id}", response_model=Expense_Public)
def delete_expense(expense_id:int, session=Depends(get_session)):
    db_expense=session.get(Expense_Table, expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    session.delete(db_expense)
    session.commit()
    return Response(status_code=204)

"""
product
"""

@app.post("/product", response_model=Product_Public)
def record_product(product: Product_Record, session=Depends(get_session)):
    db_product=Product_Table.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.get("/product", response_model=Product_List)
def get_products(offset:int=0, limit:int=100, search: str = Query(None), session=Depends(get_session)):
    query = session.query(Product_Table)
    if search:
        query = query.filter(Product_Table.name.contains(search))
    products = query.offset(offset).limit(limit).all()
    total = query.count()
    return Product_List(items=products, total=total, offset=offset, limit=limit)

@app.get("/product/{product_id}", response_model=Product_Public)
def get_product(product_id:int, session=Depends(get_session)):
    product=session.get(Product_Table, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/product/{product_id}", response_model=Product_Public)
def update_product(product_id:int, product: Product_Update, session=Depends(get_session)):  
    db_product=session.get(Product_Table, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_data=product.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.delete("/product/{product_id}", response_model=Product_Public)
def delete_product(product_id:int, session=Depends(get_session)):
    db_product=session.get(Product_Table, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(db_product)
    session.commit()
    return Response(status_code=204)

"""
products
"""

@app.post("/products", response_model=Products_Public)
def record_products(products: Products_Record, session=Depends(get_session)):
    db_products=Products_Table.model_validate(products)
    session.add(db_products)
    session.commit()
    session.refresh(db_products)
    return db_products

@app.get("/products", response_model=Products_List)
def get_products(offset:int=0, limit:int=100, search: str = Query(None  ), session=Depends(get_session)):
    query = session.query(Products_Table)
    if search:
        query = query.filter(Products_Table.name.contains(search))
    products = query.offset(offset).limit(limit).all()
    total = query.count()
    return Products_List(items=products, total=total, offset=offset, limit=limit)

@app.get("/products/{products_id}", response_model=Products_Public)
def get_products(products_id:int, session=Depends(get_session)):        
    products=session.get(Products_Table, products_id)
    if not products:
        raise HTTPException(status_code=404, detail="Products not found")
    return products

@app.put("/products/{products_id}", response_model=Products_Public)
def update_products(products_id:int, products: Products_Update, session=Depends(get_session)):  
    db_products=session.get(Products_Table, products_id)
    if not db_products:
        raise HTTPException(status_code=404, detail="Products not found")
    products_data=products.model_dump(exclude_unset=True)
    for key, value in products_data.items():
        setattr(db_products, key, value)
    session.add(db_products)
    session.commit()
    session.refresh(db_products)
    return db_products

@app.delete("/products/{products_id}", response_model=Products_Public)
def delete_products(products_id:int, session=Depends(get_session)):
    db_products=session.get(Products_Table, products_id)
    if not db_products:
        raise HTTPException(status_code=404, detail="Products not found")
    session.delete(db_products)
    session.commit()
    return Response(status_code=204)

"""
Income
"""
@app.post("/income", response_model=Income_Public)
def record_income(income: Income_Record, session=Depends(get_session)):
    db_income=Income_Table.model_validate(income)
    session.add(db_income)
    session.commit()
    session.refresh(db_income)
    return db_income

@app.get("/income", response_model=Income_List)
def get_incomes(offset:int=0, limit:int=100, search: str = Query(None), session=Depends(get_session)):
    query = session.query(Income_Table)
    if search:
        query = query.filter(Income_Table.name.contains(search))
    incomes = query.offset(offset).limit(limit).all()
    total = query.count()
    return Income_List(items=incomes, total=total, offset=offset, limit=limit)

@app.get("/income/{income_id}", response_model=Income_Public)
def get_income(income_id:int, session=Depends(get_session)):
    income=session.get(Income_Table, income_id)
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    return income

@app.put("/income/{income_id}", response_model=Income_Public)
def update_income(income_id:int, income: Income_Update, session=Depends(get_session)):  
    db_income=session.get(Income_Table, income_id)
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    income_data=income.model_dump(exclude_unset=True)
    for key, value in income_data.items():
        setattr(db_income, key, value)
    session.add(db_income)
    session.commit()
    session.refresh(db_income)
    return db_income

@app.delete("/income/{income_id}", response_model=Income_Public)
def delete_income(income_id:int, session=Depends(get_session)):
    db_income=session.get(Income_Table, income_id)
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    session.delete(db_income)
    session.commit()
    return Response(status_code=204)

"""
expenses
"""

@app.post("/expenses", response_model=Expenses_Public)
def record_expenses(expenses: Expenses_Record, session=Depends(get_session)):
    db_expenses=Expenses_Table.model_validate(expenses)
    session.add(db_expenses)
    session.commit()
    session.refresh(db_expenses)
    return db_expenses

@app.get("/expenses", response_model=Expenses_List)
def get_expenses(offset:int=0, limit:int=100, search: str = Query(None), session=Depends(get_session)):
    query = session.query(Expenses_Table)
    if search:
        query = query.filter(Expenses_Table.name.contains(search))
    expenses = query.offset(offset).limit(limit).all()
    total = query.count()
    return Expenses_List(items=expenses, total=total, offset=offset, limit=limit)
