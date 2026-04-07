from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.services.role_service import (
    create_role,
    get_roles,
    get_role_by_id,
    update_role_by_id,
    delete_role_by_id
)
from app.authentication.auth import get_current_user
from app.policies.base_policy import BasePolicy

router = APIRouter(prefix="/roles")


def get_role_or_404(role_id: int, db: Session = Depends(get_db)):
    role = get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


def _authorize_admin(current_user):
    """
    Проверка, что пользователь имеет полный доступ к категории 'roles'.
    """
    policy = BasePolicy(current_user)
    policy.can_create("roles")

@router.get("/", response_model=List[RoleResponse])
def index(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    _authorize_admin(current_user)
    return get_roles(db)


@router.get("/{role_id}", response_model=RoleResponse)
def show(role: Role = Depends(get_role_or_404), current_user = Depends(get_current_user)):
    _authorize_admin(current_user)
    return role


@router.post("/", response_model=RoleResponse, status_code=201)
def create(role_data: RoleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    _authorize_admin(current_user)
    try:
        return create_role(db, role_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{role_id}", response_model=RoleResponse)
def update(role_data: RoleUpdate, role: Role = Depends(get_role_or_404), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    _authorize_admin(current_user)
    try:
        return update_role_by_id(db, role.id, role_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{role_id}", status_code=204)
def destroy(role: Role = Depends(get_role_or_404), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    _authorize_admin(current_user)
    delete_role_by_id(db, role.id)
