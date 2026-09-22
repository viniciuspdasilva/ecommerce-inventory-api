from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float

from src.infra.database import Base


# --- Entities (SQLAlchemy) ---

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    title = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    category = Column(String)
    image = Column(String)

    rating_rate = Column(Float)
    rating_count = Column(Integer)

    @property
    def rating(self):
        return {
            "rate": self.rating_rate,
            "count": self.rating_count
        }


# --- Schemas (Pydantic) ---

class RatingSchema(BaseModel):
    rate: float
    count: int

class ProductCreate(BaseModel):
    title: str
    price: float
    description: str
    category: str
    image: str
    rating: RatingSchema

class ProductUpdate(BaseModel):
    price: Optional[float] = None
    category: Optional[str] = None
    rating: Optional[RatingSchema] = None

class ProdutoResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True