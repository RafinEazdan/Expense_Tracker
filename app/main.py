import utils
from database import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Response
from psycopg import Connection
from psycopg.errors import UniqueViolation
import schemas
from typing import List
from routers import reports


app = FastAPI()


app.include_router(reports.router)


@app.get("/")
async def root():

    return{"message":"Website is UP!"}




# -------------------USERS---------------------
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
        








