from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.user import User
from app.models.category import Category
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)
from app.services.category_service import (
    create_category,
    get_categories,
    get_category_by_id,
    update_category_by_id,
    delete_category_by_id,
)
from app.authentication.auth import get_current_user


router = APIRouter(prefix="/categories", tags=["Categories"])


def admin_required(current_user: User):
    if not current_user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Access denied")


def get_category_or_404(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/", response_model=List[CategoryResponse])
def index(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    admin_required(current_user)
    return get_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def show(
    category: Category = Depends(get_category_or_404),
    current_user: User = Depends(get_current_user),
):
    admin_required(current_user)
    return category


@router.post("/", response_model=CategoryResponse, status_code=201)
def create(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    admin_required(current_user)

    try:
        return create_category(db, category_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{category_id}", response_model=CategoryResponse)
def update(
    category_update: CategoryUpdate,
    category: Category = Depends(get_category_or_404),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    admin_required(current_user)

    try:
        return update_category_by_id(db, category.id, category_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{category_id}", status_code=204)
def destroy(
    category: Category = Depends(get_category_or_404),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    admin_required(current_user)
    delete_category_by_id(db, category.id)
