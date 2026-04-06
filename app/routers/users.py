from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import create_user, get_users, get_user_by_id, delete_user_by_id, update_user_by_id

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def index(db: Session = Depends(get_db)):
    users = get_users(db)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
def show(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=UserResponse, status_code=201)
def create(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/users/{user_id}", response_model=UserResponse)
def update(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    try:
        updated_user = update_user_by_id(db, user_id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/users/{user_id}", status_code=204)
def destroy(user_id: int, db: Session = Depends(get_db)):
    deleted = delete_user_by_id(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
