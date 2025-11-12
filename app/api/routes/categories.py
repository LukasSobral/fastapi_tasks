from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.crud import crud_category
from app.api.deps import get_db, get_current_user
from app.db.models import User

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_category.create_category(db=db, category=category, owner_id=current_user.id)

@router.get("/", response_model=list[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista categorias do usuário autenticado.
    """
    return crud_category.get_all_categories(db=db, owner_id=current_user.id)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza o nome de uma categoria.
    """
    category = crud_category.update_category(db, category_id, category_update)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Deleta uma categoria (apenas usuários autenticados).
    """
    category = crud_category.delete_category(db=db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return {"ok": True, "message": f"Categoria '{category.name}' removida com sucesso."}
