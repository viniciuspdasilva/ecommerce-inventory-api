from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float

from src.infra.database import Base


# --- Entities (SQLAlchemy) ---

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    description: str = Column(String, nullable=True)
    category = Column(String)
    image: str = Column(String, nullable=True)



# --- Schemas (Pydantic) ---

class ProductCreate(BaseModel):
    title: str
    price: float
    description: str
    category: str
    image: str

class ProductUpdate(BaseModel):
    price: Optional[float] = None
    category: Optional[str] = None

class ProdutoResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True