from app.database import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
# from psycopg import Connection
# from psycopg.errors import UniqueViolation
from .routers import reports, users, auth, llm


app = FastAPI()
# CORS Configuration
origins = [
    "http://localhost:5173",  # Local development
    "https://expense-tracker-self-mu-50.vercel.app",  # Production deployment
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reports.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(llm.router)

@app.get("/")
async def root():

    return{"message":"Website is UP! try Nowwwwwww. yayayayaay. You sure? Yes absolutely!!"}
