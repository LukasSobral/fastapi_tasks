from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.task import TaskCreate, TaskResponse,TaskUpdate
from app.crud import crud_task
from app.api.deps import get_db, get_current_user
from app.db.models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/summary")
def get_task_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna um resumo das tarefas do usuário autenticado.
    """
    summary = crud_task.get_task_summary(db=db, user_id=current_user.id)
    return summary


@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_task.create_task(db=db, task=task, user_id=current_user.id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = crud_task.update_task(db, task_id, current_user.id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada ou não pertence a este usuário")
    return task


@router.get("/", response_model=list[TaskResponse])
def read_tasks(
    skip: int = 0,
    limit: int = 10,
    completed: Optional[bool] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista tarefas do usuário autenticado, com filtros opcionais:
    - ?completed=true
    - ?category_id=2
    - ?skip=0&limit=10
    """
    tasks = crud_task.get_tasks(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        completed=completed,
        category_id=category_id,
    )
    return tasks

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = crud_task.delete_task(db=db, task_id=task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada ou não pertence a este usuário")
    return {"ok": True, "message": f"Tarefa {task_id} removida"}
