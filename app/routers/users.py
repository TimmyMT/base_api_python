from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    delete_user_by_id,
    update_user_by_id,
)
from app.params.user_params import validate_create_params, validate_update_params

router = APIRouter()

def get_user_or_404(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users", response_model=List[UserResponse])
def index(db: Session = Depends(get_db)):
    return get_users(db)


@router.get("/users/{user_id}", response_model=UserResponse)
def show(user = Depends(get_user_or_404)):
    return user


@router.post("/users", response_model=UserResponse, status_code=201)
def create(user: UserCreate, db: Session = Depends(get_db)):
    validate_create_params(user)
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/users/{user_id}", response_model=UserResponse)
def update(user_update: UserUpdate, user = Depends(get_user_or_404), db: Session = Depends(get_db)):
    validate_update_params(user_update)
    try:
        return update_user_by_id(db, user.id, user_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/users/{user_id}", status_code=204)
def destroy(user = Depends(get_user_or_404), db: Session = Depends(get_db)):
    delete_user_by_id(db, user.id)
