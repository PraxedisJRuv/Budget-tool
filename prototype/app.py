from fastapi import FastAPI, HTTPException, Response, Depends, Query
from utils import create_db, get_session
from models import *
app=FastAPI()

create_db()


"""

"""
@app.post("/buy")
def record_buy(buy: Buy_Record, session=Depends(get_session)):
    db_buy=Buys_Table.model_validate(buy)
    session.add(db_buy)
    #We should add the expense when adding a buy
    session.commit()
    session.refresh(db_buy)
    return db_buy