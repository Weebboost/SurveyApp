import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from datetime import datetime

class UserBase(SQLModel):
    email: EmailStr = Field(unique = True, index = True, max_length=255)
    role: str = Field(default="user")

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserPublic(UserBase):
    created_at: datetime

class User(UserBase, table = True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime
    is_active: bool