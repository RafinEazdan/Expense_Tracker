import utils
from database import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Response
from psycopg import Connection
from psycopg.errors import UniqueViolation
import schemas
from typing import List
from routers import reports, users


app = FastAPI()


app.include_router(reports.router)
app.include_router(users.router)

@app.get("/")
async def root():

    return{"message":"Website is UP!"}


     
        








