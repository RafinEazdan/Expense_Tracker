import secrets
import json
from jinja2 import DictLoader
from app.oauth import get_current_user
import app.utils as utils
from app.database import get_db
from fastapi import Depends, HTTPException, status, Response, APIRouter
from psycopg import Connection
from psycopg.errors import UniqueViolation
import app.schemas as schemas
from typing import List
from app.redis.depends import get_redis

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

@router.post('/', status_code=status.HTTP_202_ACCEPTED)
async def post_users( user:schemas.UserCreate, db: Connection = Depends(get_db), redis = Depends(get_redis)):
     # Redis
     with db.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE email = %s;", (user.email,))
        existing_user = cursor.fetchone()
        
     if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email already registered. Please login."
        )


     # Hashing the Password
     hashed_pass = utils.hash(user.password)
     otp_code = f"{secrets.randbelow(1000000):06d}"
     registration_data = {
        "email": user.email,
        "hashed_password": hashed_pass,
        "otp": otp_code
    }
     print(f"Generated OTP for {user.email}: {otp_code}")  # For debugging purposes, remove in production
     await redis.set(f"reg:{user.email}", json.dumps(registration_data), expire=600)
     return {"message": "OTP sent to email. Please verify to complete registration."}


@router.post('/verify-otp', response_model=schemas.UserResponse)
async def verify_registration(verify_req:schemas.verifyOTPRequest, db: Connection = Depends(get_db), redis=Depends(get_redis)):
    raw_data = await redis.get(f"reg:{verify_req.email}")
    if not raw_data:
        raise HTTPException(status_code=404, detail="Registration expired or not found")
    
    user_data = json.loads(raw_data)
    
    if user_data['otp'] != verify_req.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (email, hashed_password) VALUES (%s, %s) RETURNING id, email, created_at;",
                (user_data['email'], user_data['hashed_password'])
            )
            new_user = cursor.fetchone()
        db.commit()
        
        await redis.delete(f"reg:{verify_req.email}")
        
        return new_user
    except UniqueViolation:
        db.rollback()
        raise HTTPException(status_code=409, detail="User already exists")


@router.get('/profile', response_model=schemas.UserResponse)
def get_users(db: Connection = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["id"] is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You must login first!')
    with db.cursor() as cursor:
        cursor.execute(''' SELECT * from users where id = %s; ''', (current_user["id"],))
        users = cursor.fetchone()
    if users is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User details is unavailable')
    return users

@router.delete('/profile/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_users(db: Connection = Depends(get_db), current_user: DictLoader = Depends(get_current_user)):
    with db.cursor() as cursor:
        cursor.execute('Delete from users where id = %s;',(current_user["id"],))
        deleted_user = cursor.rowcount

    db.commit()

    if deleted_user == 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not logged in!")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)