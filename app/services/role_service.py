from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate
from typing import List


def get_roles(db: Session) -> List[Role]:
    return db.query(Role).all()


def get_role_by_id(db: Session, role_id: int) -> Role | None:
    return db.query(Role).filter(Role.id == role_id).first()


def create_role(db: Session, role_data: RoleCreate) -> Role:
    # проверяем уникальность
    existing = db.query(Role).filter(Role.name == role_data.name).first()
    if existing:
        raise ValueError(f"Role '{role_data.name}' already exists")
    role = Role(name=role_data.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role_by_id(db: Session, role_id: int, role_data: RoleUpdate) -> Role:
    role = get_role_by_id(db, role_id)
    if not role:
        raise ValueError("Role not found")
    # проверяем уникальность нового имени
    existing = db.query(Role).filter(Role.name == role_data.name, Role.id != role_id).first()
    if existing:
        raise ValueError(f"Role '{role_data.name}' already exists")
    role.name = role_data.name
    db.commit()
    db.refresh(role)
    return role


def delete_role_by_id(db: Session, role_id: int):
    role = get_role_by_id(db, role_id)
    if not role:
        raise ValueError("Role not found")
    db.delete(role)
    db.commit()


# ----------------- Логика назначения и снятия роли пользователю -----------------

def assign_role_to_user(db: Session, user: User, role: Role):
    if role in user.roles:
        raise ValueError("User already has this role")
    user.roles.append(role)
    db.commit()
    db.refresh(user)
    return user


def revoke_role_from_user(db: Session, user: User, role: Role):
    if role not in user.roles:
        raise ValueError("User does not have this role")
    user.roles.remove(role)
    db.commit()
    db.refresh(user)
    return user
