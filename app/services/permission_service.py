from sqlalchemy.orm import Session
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate

def create_permission(db: Session, data: PermissionCreate) -> Permission:
    permission = Permission(**data.dict())
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

def get_permissions(db: Session):
    return db.query(Permission).all()

def get_permission_by_id(db: Session, permission_id: int):
    return db.query(Permission).filter(Permission.id == permission_id).first()

def update_permission_by_id(db: Session, permission_id: int, data: PermissionUpdate):
    permission = get_permission_by_id(db, permission_id)
    if not permission:
        raise ValueError("Permission not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(permission, field, value)
    db.commit()
    db.refresh(permission)
    return permission

def delete_permission_by_id(db: Session, permission_id: int):
    permission = get_permission_by_id(db, permission_id)
    if not permission:
        raise ValueError("Permission not found")
    db.delete(permission)
    db.commit()
