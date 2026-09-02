from sqlalchemy.orm import Session

from src.domain.models import ProductCreate, Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, product: ProductCreate):
        new_product = Product(**product.model_dump())
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def list(self):
        return self.db.query(Product).all()

    def find_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def update(self, product_id: int, product: ProductCreate):
        self.db.query(Product).filter(Product.id == product_id).update(product.model_dump())
        self.db.commit()
        return self.find_by_id(product_id)

    def delete(self, product_id: int):
        self.db.query(Product).filter(Product.id == product_id).delete()
        self.db.commit()