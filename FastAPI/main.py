from ast import List
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ['*']
)





class TransactionBase(BaseModel):
    amount : float
    category : str
    description : str
    is_income : bool
    date : str

class TransactionModel(TransactionBase):
    id : int

    class Config:
        from_attributes = True

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]




@app.post("/transactions", response_model=TransactionModel)
async def create_transaction(transaction: TransactionBase, db: db_dependency):
    """
    amount = Column(Float)
    category = Column(String)
    description = Column(String)
    is_income = Column(Boolean)
    date = Column(String)
    """
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@app.get("/transactions" , response_model=list[TransactionModel])
async def read_transactions(db: db_dependency, skip : int = 0, limit : int = 100):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions







# @app.get("/")
# def say():
#     return "hello world"


















