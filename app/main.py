from database import get_db
from fastapi import FastAPI, Depends, HTTPException, status
from psycopg import Connection
import schemas
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

@app.post('/users')
def post_users():
     return