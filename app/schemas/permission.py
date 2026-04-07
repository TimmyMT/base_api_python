# app/schemas/permission.py
from pydantic import BaseModel

class PermissionBase(BaseModel):
    role_id: int
    category_id: int
    can_read: bool = False
    can_create: bool = False
    can_update: bool = False
    can_delete: bool = False

class PermissionCreate(PermissionBase):
    role_id: int
    category_id: int
    can_read: bool = False
    can_create: bool = False
    can_update: bool = False
    can_delete: bool = False

class PermissionUpdate(BaseModel):
    can_read: bool | None = None
    can_create: bool | None = None
    can_update: bool | None = None
    can_delete: bool | None = None

class PermissionResponse(PermissionBase):
    id: int

    class Config:
        orm_mode = True
