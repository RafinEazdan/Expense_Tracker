from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ExpenseReport(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: Optional[str] = None
    created_at: datetime
    owner_id: int
    class Config:
        from_attributes = True


class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]  = None


class LLMxSQL(BaseModel):
    query: str