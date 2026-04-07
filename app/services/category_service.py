from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_categories(db: Session):
    return db.query(Category).all()


def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()


def create_category(db: Session, category_data: CategoryCreate):
    existing_category = get_category_by_name(db, category_data.name)

    if existing_category:
        raise ValueError("Category already exists")

    category = Category(name=category_data.name)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def update_category_by_id(
    db: Session,
    category_id: int,
    category_update: CategoryUpdate
):
    category = get_category_by_id(db, category_id)

    if not category:
        return None

    existing_category = get_category_by_name(db, category_update.name)

    if existing_category and existing_category.id != category.id:
        raise ValueError("Category name already exists")

    category.name = category_update.name

    db.commit()
    db.refresh(category)

    return category


def delete_category_by_id(db: Session, category_id: int):
    category = get_category_by_id(db, category_id)

    if not category:
        return False

    db.delete(category)
    db.commit()

    return True
