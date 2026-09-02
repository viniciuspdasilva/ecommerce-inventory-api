from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.domain.models import ProdutoResponse, ProductCreate
from src.infra.database import get_db
from src.infra.repositories import ProductRepository

# Cria o roteador do FastAPI
router = APIRouter(prefix="/products", tags=["Estoque de Produtos"])

@router.get("/", response_model=List[ProdutoResponse])
def list_products(db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return repo.list()

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return repo.create(product)

@router.get("/{product_id}", response_model=ProdutoResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.find_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.put("/{product_id}", response_model=ProdutoResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.update(product_id, product)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return repo.update(product_id, product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.delete(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    repo.delete(product_id)
