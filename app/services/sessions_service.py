from datetime import datetime, timedelta
import jwt
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.refresh_token import RefreshToken
from app.models.user import User

# --- приватные функции для работы с паролями через Argon2 ---
_pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def _verify_password(password: str, hashed: str) -> bool:
    return _pwd_context.verify(password, hashed)

# --- настройки JWT ---
_JWT_SECRET = "supersecretkey"
_JWT_ALGORITHM = "HS256"
_ACCESS_TOKEN_EXPIRE_MINUTES = 60
_REFRESH_TOKEN_EXPIRE_MINUTES = 120

# --- приватные функции для токенов ---
def _generate_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=_ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALGORITHM)

def _generate_refresh_token(db: Session, user_id: int) -> str:
    token_str = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=_REFRESH_TOKEN_EXPIRE_MINUTES)
    db_token = RefreshToken(
        user_id=user_id,
        token=token_str,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return token_str

def _validate_refresh_token(db: Session, refresh_token: str) -> RefreshToken:
    token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.revoked == False
    ).first()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    if token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    return token

# --- публичные функции ---
def create(db: Session, email: str, password: str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user or not _verify_password(password, user.password_digest):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )

    access_token = _generate_access_token(user.id)
    refresh_token = _generate_refresh_token(db, user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def update(db: Session, refresh_token: str) -> dict:
    token = _validate_refresh_token(db, refresh_token)
    user = token.user

    access_token = _generate_access_token(user.id)
    refresh_token = _generate_refresh_token(db, user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def destroy(db: Session, refresh_token: str) -> bool:
    token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.revoked == False
    ).first()
    if token:
        token.revoked = True
        db.commit()
        return True
    return False
