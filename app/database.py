import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
import time

load_dotenv()

def get_db():
    while True:
        try:
            conn = psycopg.connect(
            host=os.getenv("HOST_DB"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("USER_DB"),
            password=os.getenv("PASSWORD"),
            port=os.getenv("DB_PORT"),
            row_factory=dict_row
        )
            print("DB is connected!!!!!!")
            break
        except Exception as e:
            print("DB Connection Failed.\nError= ",e)
            time.sleep(2)

    try:
        yield conn

    finally:
        conn.close()