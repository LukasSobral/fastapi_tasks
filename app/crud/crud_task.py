from sqlalchemy.orm import Session
from app.db import models
from app.schemas.task import TaskCreate, TaskUpdate
from typing import Optional, List
from sqlalchemy import func
from datetime import datetime


def create_task(db: Session, task: TaskCreate, user_id: int):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        category_id=task.category_id,
        owner_id=user_id,
        completed=False,
        completed_at=None
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_summary(db: Session, user_id: int):
    total = db.query(models.Task).filter(models.Task.owner_id == user_id).count()

    completed = db.query(models.Task).filter(
        models.Task.owner_id == user_id,
        models.Task.completed == True
    ).count()

    pending = total - completed

    results = (
        db.query(models.Category.name, func.count(models.Task.id))
        .join(models.Task, models.Category.id == models.Task.category_id)
        .filter(models.Task.owner_id == user_id)
        .group_by(models.Category.name)
        .all()
    )

    by_category = {name: count for name, count in results}

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "by_category": by_category,
    }


def update_task(db: Session, task_id: int, user_id: int, task_update: TaskUpdate):
    task = get_task(db, task_id, user_id)
    if not task:
        return None

    # completed_at correto
    if task_update.completed is not None:
        if task_update.completed is True and task.completed_at is None:
            task.completed_at = datetime.utcnow()
        elif task_update.completed is False:
            task.completed_at = None

    # aplicar mudanças
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task
def get_task(db: Session, task_id: int, user_id: int):
    return db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user_id
    ).first()

def get_tasks(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    category_id: Optional[int] = None,
) -> List[models.Task]:

    query = db.query(models.Task).filter(models.Task.owner_id == user_id)

    if completed is not None:
        query = query.filter(models.Task.completed == completed)

    if category_id is not None:
        query = query.filter(models.Task.category_id == category_id)

    return query.offset(skip).limit(limit).all()

def delete_task(db: Session, task_id: int, user_id: int):
    task = get_task(db, task_id, user_id)
    if task:
        db.delete(task)
        db.commit()
    return task
