from fastapi import HTTPException
from app.schemas.user import UserCreate, UserUpdate

def validate_create_params(user: UserCreate):
    """Strong params for create: ensure required fields are present."""
    if not user.email or not user.password or not user.password_confirmation:
        raise HTTPException(status_code=400, detail="Missing required fields: email, password, password_confirmation")

def validate_update_params(user_update: UserUpdate):
    """Strong params for update: ensure at least one field and password_confirmation if password."""
    if user_update.email is None and user_update.password is None:
        raise HTTPException(status_code=400, detail="At least one field (email or password) must be provided")
    if user_update.password and not user_update.password_confirmation:
        raise HTTPException(status_code=400, detail="password_confirmation is required when updating password")
