import utils
from database import get_db
from fastapi import FastAPI, Depends, HTTPException, status
from psycopg import Connection
from psycopg.errors import UniqueViolation
import schemas
from typing import List
app = FastAPI()

@app.get("/")
async def root():

    return{"message":"Website is UP!"}

@app.get('/users')
def get_users(db: Connection = Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(''' SELECT * from users ''')
        users = cursor.fetchall()
    return users

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def post_users( user:schemas.UserCreate, db: Connection = Depends(get_db)):
     # Hashing the Password
     hashed_pass = utils.hash(user.password)
     user.password = hashed_pass
     try:
        with db.cursor() as cursor:
            cursor.execute('''Insert into users (email, hashed_password) VALUES (%s, %s) RETURNING id, email, created_at;''', (user.email, hashed_pass))
            new_user = cursor.fetchone()
        db.commit()
        return new_user

     except UniqueViolation:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email Already Registered. Try login!")
        




# ----------------Expense Reports--------------------
@app.get('/expenses', response_model=List[schemas.ExpenseResponse])
def get_expenses(db: Connection = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute('''SELECT * from expenses;''')
            Expenses = cursor.fetchall()
        return Expenses

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts Not Found!")


@app.post('/expenses', response_model=schemas.ExpenseResponse)
def get_expenses(expenses: schemas.ExpenseReport, db: Connection = Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute('''Insert into expenses (amount, category, description) VALUES (%s, %s, %s) RETURNING *''',(expenses.amount, expenses.category, expenses.description))
            Expenses = cursor.fetchone()
        db.commit()
        return Expenses

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Post cannot be posted! Error is {e}")
    