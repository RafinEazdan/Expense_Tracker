from sqlalchemy import create_engine, MetaData
import os
from dotenv import load_dotenv

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(bind=engine)
