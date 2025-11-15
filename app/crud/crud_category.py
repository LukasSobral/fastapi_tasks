from sqlalchemy.orm import Session
from app.db import models
from app.schemas.category import CategoryCreate, CategoryUpdate

def create_category(db: Session, category: CategoryCreate, owner_id: int):
    db_cat = models.Category(
        name=category.name,
        owner_id=owner_id
    )
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


def get_all_categories(db: Session, owner_id: int):
    """Retorna apenas as categorias do usuário autenticado"""
    return (
        db.query(models.Category)
        .filter(models.Category.owner_id == owner_id)
        .all()
    )


def get_category_by_id(db: Session, category_id: int):
    """Busca uma categoria específica"""
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def update_category(db: Session, category_id: int, category_update: CategoryUpdate):
    category = get_category_by_id(db, category_id)
    if not category:
        return None

    for field, value in category_update.model_dump(exclude_unset=True).items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    """Remove uma categoria"""
    category = get_category_by_id(db, category_id)
    if category:
        db.delete(category)
        db.commit()
    return category
