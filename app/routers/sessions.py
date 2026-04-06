from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status
from pydantic import BaseModel

from app.db import get_db
from app.services.sessions_service import create, destroy, update

router = APIRouter()

# Схема запроса и ответа для логина
class SignInRequest(BaseModel):
    email: str
    password: str

class LogoutRequest(BaseModel):
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

# POST /login
@router.post("/sessions/login", response_model=TokenResponse)
def sign_in(data: SignInRequest, db: Session = Depends(get_db)):
    return create(db, email=data.email, password=data.password)

# PUT /refresh
@router.put("/sessions/refresh", response_model=dict)
def update_access_token(request: RefreshRequest, db: Session = Depends(get_db)):
    try:
        tokens = update(db, request.refresh_token)
        return tokens
    except HTTPException as e:
        raise e

# DELETE /logout
@router.delete("/sessions/logout", status_code=204)
def logout(request: LogoutRequest, db: Session = Depends(get_db)):
    destroyed = destroy(db, request.refresh_token)
    if destroyed is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found or already revoked"
        )
