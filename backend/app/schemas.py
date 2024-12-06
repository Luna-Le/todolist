from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 

class Category(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True) 

class Task(BaseModel):
    name: str
    completed: bool = False
    category: str
    model_config = ConfigDict(from_attributes=True) 

class TaskOut(BaseModel):
    id: int
    name: str
    completed: bool
    category: Category
    model_config = ConfigDict(from_attributes=True) 

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



