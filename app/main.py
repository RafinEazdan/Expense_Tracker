import utils
from database import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Response
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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Expense cannot be posted! Error: {e}")
    
@app.get('/expenses/{id}', response_model=schemas.ExpenseResponse)
def get_a_expense_report(id: int, db: Connection = Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute('''SELECT * from expenses where id = %s;''',(id,))
        report = cursor.fetchone()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested Expense Report Cannot be found. Try again!") 
    
    return report

@app.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(id: int, db: Connection = Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute('''Delete from expenses where id = %s;''',(id,))
        deleted_report = cursor.rowcount
    db.commit()
    if deleted_report == 0:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested Expense Report Cannot be found. Try again!")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/expenses/{id}", response_model=schemas.ExpenseResponse)
def update_report(id: int, expense_report: schemas.ExpenseReport,  db: Connection = Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute('UPDATE expenses SET amount=%s, category=%s, description=%s WHERE id=%s RETURNING *',(expense_report.amount, expense_report.category, expense_report.description, id))
        updated_report = cursor.fetchone()
        db.commit()

    if updated_report is None:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Requested Expense Report Cannot be found. Try again!')
    return updated_report



