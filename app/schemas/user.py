from pydantic import BaseModel, EmailStr, Field, validator
import re
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=5, max_length=72)

    @validator('email')
    def validate_email(cls, v):
        # Дополнительная проверка email с regex, хотя EmailStr уже проверяет базово
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=5, max_length=72)

    @validator('email')
    def validate_email(cls, v):
        if v is None:
            return v
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v
