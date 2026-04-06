from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def create_user(db: Session, user: UserCreate):
    # Проверяем, существует ли пользователь с таким email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Хэшируем пароль
    hashed_password = pwd_context.hash(user.password)
    
    db_user = User(email=user.email, password_digest=hashed_password)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this email already exists")
