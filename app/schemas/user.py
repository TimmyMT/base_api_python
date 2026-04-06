from pydantic import BaseModel, EmailStr, Field, validator
import re
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=5, max_length=72)
    password_confirmation: str

    @validator('email')
    def validate_email(cls, v):
        # Дополнительная проверка email с regex, хотя EmailStr уже проверяет базово
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v

    @validator('password_confirmation')
    def validate_password_confirmation(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Password confirmation does not match password')
        return v

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=5, max_length=72)
    password_confirmation: Optional[str] = None

    @validator('email')
    def validate_email(cls, v):
        if v is None:
            return v
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')
        return v

    @validator('password_confirmation')
    def validate_password_confirmation(cls, v, values):
        if v is not None and 'password' in values and values['password'] is not None:
            if v != values['password']:
                raise ValueError('Password confirmation does not match password')
        return v
