from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserRoleUpdate
from app.services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    delete_user_by_id,
    update_user_by_id,
)
from app.params.user_params import validate_create_params, validate_update_params
from app.authentication.auth import get_current_user
from app.policies.base_policy import BasePolicy

router = APIRouter(prefix="/users")


def get_user_or_404(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def _authorize(current_user: User, category_name: str, action: str, target_user: User = None):
    policy = BasePolicy(current_user)

    # если операция на своем ресурсе
    if target_user and target_user.id == current_user.id:
        return policy.can_own(target_user.id)

    if action == "read":
        return policy.can_read(category_name)
    elif action == "write":
        return policy.can_write(category_name)
    elif action == "delete":
        return policy.can_delete(category_name)
    else:
        raise HTTPException(status_code=403, detail="Unknown action")


# ------------------ ROUTES ------------------

@router.get("/", response_model=List[UserResponse])
def index(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    _authorize(current_user, "users", "read")
    return get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def show(
    user: User = Depends(get_user_or_404),
    current_user: User = Depends(get_current_user)
):
    _authorize(current_user, "users", "read", user)
    return user


@router.post("/", response_model=UserResponse, status_code=201)
def create(
    user_create: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    _authorize(current_user, "users", "create")
    validate_create_params(user_create)
    try:
        return create_user(db, user_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
def update(
    user_update: UserUpdate,
    user: User = Depends(get_user_or_404),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    _authorize(current_user, "users", "update", user)
    validate_update_params(user_update)
    try:
        return update_user_by_id(db, user.id, user_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", status_code=204)
def destroy(
    user: User = Depends(get_user_or_404),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    _authorize(current_user, "users", "delete", user)
    delete_user_by_id(db, user.id)
