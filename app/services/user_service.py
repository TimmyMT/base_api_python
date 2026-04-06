from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

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

def update_user_by_id(db: Session, user_id: int, user_update: UserUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    if user_update.email is not None:
        # Проверяем, не занят ли email другим пользователем
        existing = db.query(User).filter(User.email == user_update.email, User.id != user_id).first()
        if existing:
            raise ValueError("User with this email already exists")
        user.email = user_update.email
    if user_update.password is not None:
        user.password_digest = pwd_context.hash(user_update.password)
    db.commit()
    db.refresh(user)
    return user

def delete_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_active = False
        db.commit()
        db.refresh(user)
        return True
    return False
