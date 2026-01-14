from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String, text

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, nullable=False)
    amount = Column(Float,nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"))





