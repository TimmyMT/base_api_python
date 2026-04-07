from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.role import Role
from app.models.user import User
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.schemas.role import RoleAssignRequest
from app.services.role_service import (
    create_role,
    get_roles,
    get_role_by_id,
    update_role_by_id,
    delete_role_by_id,
    assign_role_to_user,
    revoke_role_from_user,
)
from app.services.user_service import get_user_by_id
from app.authentication.auth import get_current_user
from app.policies.base_policy import BasePolicy

router = APIRouter(prefix="/roles", tags=["Roles"])


# ----------------- HELPERS -----------------

def _authorize_admin(user: User):
    policy = BasePolicy(user)
    policy.can_create("roles")


def _get_role_or_404(role_id: int, db: Session) -> Role:
    role = get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


def _get_user_or_404(user_id: int, db: Session) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ----------------- CRUD -----------------

@router.get("/", response_model=List[RoleResponse])
def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _authorize_admin(current_user)
    return get_roles(db)


@router.get("/{role_id}", response_model=RoleResponse)
def show(role_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _authorize_admin(current_user)
    role = _get_role_or_404(role_id, db)
    return role


@router.post("/", response_model=RoleResponse, status_code=201)
def create(role_data: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _authorize_admin(current_user)
    try:
        return create_role(db, role_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{role_id}", response_model=RoleResponse)
def update(role_id: int, role_data: RoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _authorize_admin(current_user)
    role = _get_role_or_404(role_id, db)
    try:
        return update_role_by_id(db, role.id, role_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{role_id}", status_code=204)
def destroy(role_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _authorize_admin(current_user)
    role = _get_role_or_404(role_id, db)
    delete_role_by_id(db, role.id)


# ----------------- Assign / Revoke -----------------

@router.post("/assign")
def assign_role(data: RoleAssignRequest = Body(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _authorize_admin(current_user)
    user = _get_user_or_404(data.user_id, db)
    role = _get_role_or_404(data.role_id, db)
    try:
        assign_role_to_user(db, user, role)
        return {"detail": f"Role '{role.name}' assigned to user '{user.email}'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/revoke")
def revoke_role(data: RoleAssignRequest = Body(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _authorize_admin(current_user)
    user = _get_user_or_404(data.user_id, db)
    role = _get_role_or_404(data.role_id, db)
    try:
        revoke_role_from_user(db, user, role)
        return {"detail": f"Role '{role.name}' revoked from user '{user.email}'"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
