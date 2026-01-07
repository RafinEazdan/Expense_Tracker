from oauth import get_current_user
import utils
from database import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from psycopg import Connection
from psycopg.errors import UniqueViolation
import schemas
from typing import List


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


# -------------------USERS---------------------
# get all users for admin use
# @router.get('/')
# def get_users(db: Connection = Depends(get_db)):
#     with db.cursor() as cursor:
#         cursor.execute(''' SELECT * from users; ''')
#         users = cursor.fetchall()
#     return users

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
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
     

@router.get('/{id}', response_model=schemas.UserResponse)
def get_users(id:int, db: Connection = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if id == current_user["id"]:
        with db.cursor() as cursor:
            cursor.execute(''' SELECT * from users where id = %s; ''', (id,))
            users = cursor.fetchone()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to access this information')
    return users