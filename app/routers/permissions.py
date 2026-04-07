# app/controllers/permission_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.user import User
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse
from app.services.permission_service import (
    create_permission,
    get_permissions,
    get_permission_by_id,
    update_permission_by_id,
    delete_permission_by_id,
)
from app.authentication.auth import get_current_user
from app.policies.base_policy import BasePolicy

router = APIRouter(prefix="/permissions")

def _authorize_admin(user: User):
    user.roles[0].name == "admin" or HTTPException(status_code=403, detail="Admin privileges required")


def _get_permission_or_404(permission_id: int, db: Session):
    permission = get_permission_by_id(db, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


@router.get("/", response_model=List[PermissionResponse])
def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _authorize_admin(current_user)
    return get_permissions(db)


@router.post("/", response_model=PermissionResponse, status_code=201)
def create(data: PermissionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _authorize_admin(current_user)
    try:
        return create_permission(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{permission_id}", response_model=PermissionResponse)
def update(permission_id: int, data: PermissionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _authorize_admin(current_user)
    _get_permission_or_404(permission_id, db)
    try:
        return update_permission_by_id(db, permission_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{permission_id}", status_code=204)
def destroy(permission_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _authorize_admin(current_user)
    _get_permission_or_404(permission_id, db)
    delete_permission_by_id(db, permission_id)
