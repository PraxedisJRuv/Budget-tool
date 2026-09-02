"""
All endpoints are functional, but might need some adjustments.
post buy/completed was fixed with AI, and is pending a review

The endpoints goal is to record, update and delete information (CRUD) about buys, expenses, income, etc. 
Everything expended is meant to be tracked for personal finance.
"""

from fastapi import FastAPI, HTTPException, Response, Depends, Query
from utils import create_db, get_session
from models import *
app=FastAPI()

create_db()


"""
buy
"""

@app.post("/buy/complete", response_model=BuyWithItemsResponse)
def record_buy_with_items(buy_data: BuyWithItemsRecord, session=Depends(get_session)):
    """
    Atomic transaction: Create buy + expense + items in a single operation.
    
    This ensures data integrity by:
    1. Creating the Expense record
    2. Creating the Buy record linked to the Expense
    3. Creating all Items/Products in the buy
    
    If any step fails, the entire transaction is rolled back.
    """
    try:
        # Step 1: Create expense (total cost from all items)
        total_cost = sum(item.cost * item.Quantity for item in buy_data.items)
        expense = Expense_Table(
            date=buy_data.date,
            amount=total_cost,
            concept=buy_data.expense_concept,
            description=buy_data.expense_description
        )
        session.add(expense)
        session.flush()  # Get ID without committing
        
        # Step 2: Create buy linked to expense
        buy = Buys_Table(
            date=buy_data.date,
            cost=total_cost,
            local=buy_data.local,
            business_type=buy_data.business_type,
            amount_products_type=len(buy_data.items),
            ID_expense=expense.id
        )
        session.add(buy)
        session.flush()  # Get buy ID
        
        # Step 3: Create items in buy
        created_items = []
        for item_data in buy_data.items:
            # Get or create product type
            product = session.query(Product_Table).filter_by(
                name=item_data.product_name
            ).first()
            if not product:
                product = Product_Table(name=item_data.product_name)
                session.add(product)
                session.flush()
            
            # Link item to buy
            item_in_buy = Items_Table(
                name=item_data.product_name,
                cost=item_data.cost,
                Quantity=item_data.Quantity,
                ID_product=product.id,
                ID_buy=buy.id,
                ID_expense=expense.id
            )
            session.add(item_in_buy)
            created_items.append(item_in_buy)
        
        session.commit()
        session.refresh(buy)
        session.refresh(expense)
        
        return BuyWithItemsResponse(
            buy=buy,
            expense=expense,
            items=created_items
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")

@app.post("/buy", response_model=Buy_Public)
def record_buy(buy: Buy_Record, session=Depends(get_session)):
    """
    This endpoint requires ID_expense to be already created and provided.
    Only use this for advanced workflows where you're managing transactions manually.
    For normal usage, use POST /buy/complete which handles the entire transaction atomically.
    """
    db_buy=Buys_Table.model_validate(buy)
    session.add(db_buy)
    session.commit()
    session.refresh(db_buy)
    return db_buy

@app.get("/buy", response_model=Buy_List)
def get_buys(offset:int=0, limit:int=100, search: str = Query(None), session=Depends(get_session)):
    query = session.query(Buys_Table)
    if search:
        query = query.filter(Buys_Table.local.contains(search))
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
        query = query.filter(Expense_Table.concept.contains(search))
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
Items
"""

@app.post("/Items", response_model=Items_Public)
def record_Items(Items: Items_Record, session=Depends(get_session)):
    db_Items=Items_Table.model_validate(Items)
    session.add(db_Items)
    session.commit()
    session.refresh(db_Items)
    return db_Items

@app.get("/Items", response_model=Items_List)
def get_Items(offset:int=0, limit:int=100, search: str = Query(None  ), session=Depends(get_session)):
    query = session.query(Items_Table)
    if search:
        query = query.filter(Items_Table.name.contains(search))
    Items = query.offset(offset).limit(limit).all()
    total = query.count()
    return Items_List(items=Items, total=total, offset=offset, limit=limit)

@app.get("/Items/{Items_id}", response_model=Items_Public)
def get_Item(Items_id:int, session=Depends(get_session)):        
    Items=session.get(Items_Table, Items_id)
    if not Items:
        raise HTTPException(status_code=404, detail="Items not found")
    return Items

@app.put("/Items/{Items_id}", response_model=Items_Public)
def update_Items(Items_id:int, Items: Items_Update, session=Depends(get_session)):  
    db_Items=session.get(Items_Table, Items_id)
    if not db_Items:
        raise HTTPException(status_code=404, detail="Items not found")
    Items_data=Items.model_dump(exclude_unset=True)
    for key, value in Items_data.items():
        setattr(db_Items, key, value)
    session.add(db_Items)
    session.commit()
    session.refresh(db_Items)
    return db_Items

@app.delete("/Items/{Items_id}", response_model=Items_Public)
def delete_Items(Items_id:int, session=Depends(get_session)):
    db_Items=session.get(Items_Table, Items_id)
    if not db_Items:
        raise HTTPException(status_code=404, detail="Items not found")
    session.delete(db_Items)
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
        query = query.filter(Income_Table.concept.contains(search))
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
Debt
"""
@app.post("/debt", response_model=Debt_Public)
def record_debt(debt: Debt_Record, session=Depends(get_session)):
    db_debt=Debt_Table.model_validate(debt)
    session.add(db_debt)
    session.commit()
    session.refresh(db_debt)
    return db_debt

@app.get("/debt", response_model=Debt_List)
def get_debts(offset:int=0, limit:int=100, search: str = Query(None), session=Depends(get_session)):
    query = session.query(Debt_Table)
    if search:
        query = query.filter(Debt_Table.borrower.contains(search))
    debts = query.offset(offset).limit(limit).all()
    total = query.count()
    return Debt_List(items=debts, total=total, offset=offset, limit=limit)

@app.get("/debt/{debt_id}", response_model=Debt_Public)
def get_debt(debt_id:int, session=Depends(get_session)):
    debt=session.get(Debt_Table, debt_id)
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    return debt

@app.put("/debt/{debt_id}", response_model=Debt_Public)
def update_debt(debt_id:int, debt: Debt_Update, session=Depends(get_session)):  
    db_debt=session.get(Debt_Table, debt_id)
    if not db_debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    debt_data=debt.model_dump(exclude_unset=True)
    for key, value in debt_data.items():
        setattr(db_debt, key, value)
    session.add(db_debt)
    session.commit()
    session.refresh(db_debt)
    return db_debt

@app.delete("/debt/{debt_id}", response_model=Debt_Public)
def delete_debt(debt_id:int, session=Depends(get_session)): 
    db_debt=session.get(Debt_Table, debt_id)
    if not db_debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    session.delete(db_debt)
    session.commit()
    return Response(status_code=204)