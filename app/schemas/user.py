from pydantic import BaseModel, EmailStr, Field, validator
import re

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