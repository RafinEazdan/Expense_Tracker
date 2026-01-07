import utils
from database import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from psycopg import Connection
from psycopg.errors import UniqueViolation
import schemas
from typing import List
from oauth import get_current_user



router = APIRouter(
    prefix='/expenses',
    tags=['Expense Reports']
)
# ----------------Expense Reports--------------------
@router.get('/', response_model=List[schemas.ExpenseResponse])
def get_expenses(db: Connection = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        with db.cursor() as cursor:
            cursor.execute('''SELECT * from expenses where owner_id = %s;''', (current_user['id'],))
            Expenses = cursor.fetchall()
        return Expenses

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts Not Found!")


@router.post('/', response_model=schemas.ExpenseResponse)
def get_expenses(expenses: schemas.ExpenseReport, db: Connection = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        with db.cursor() as cursor:
            cursor.execute('''Insert into expenses (amount, category, description, owner_id) VALUES (%s, %s, %s, %s) RETURNING *''',(expenses.amount, expenses.category, expenses.description, current_user['id']))
            Expenses = cursor.fetchone()
        db.commit()
        return Expenses

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Expense cannot be posted! Error: {e}")
    
@router.get('/{id}', response_model=schemas.ExpenseResponse)
def get_a_expense_report(id: int, db: Connection = Depends(get_db), current_user: int = Depends(get_current_user)):
    with db.cursor() as cursor:
        cursor.execute('''SELECT * from expenses where id = %s;''',(id,))
        report = cursor.fetchone()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested Expense Report Cannot be found. Try again!") 
    
    return report

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(id: int, db: Connection = Depends(get_db), current_user: int = Depends(get_current_user)):
    with db.cursor() as cursor:
        cursor.execute('''Delete from expenses where id = %s and owner_id=%s;''',(id,current_user["id"]))
        deleted_report = cursor.rowcount
    db.commit()
    if deleted_report == 0:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not authorized to delete this expense or it does not exist!")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.ExpenseResponse)
def update_report(id: int, expense_report: schemas.ExpenseReport,  db: Connection = Depends(get_db), current_user: int = Depends(get_current_user)):
    with db.cursor() as cursor:
        cursor.execute('UPDATE expenses SET amount=%s, category=%s, description=%s WHERE id=%s and owner_id = %s RETURNING * ',(expense_report.amount, expense_report.category, expense_report.description, id, current_user["id"]))
        updated_report = cursor.fetchone()
        db.commit()

    if updated_report is None:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You are not authorized to update this expense or it does not exist!')
    return updated_report