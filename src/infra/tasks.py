import requests

from src.domain.models import Product, ProductCreate
from src.infra.database import SessionLocal
from src.infra.repositories import ProductRepository

URL_FAKE_STORE_API = "https://fakestoreapi.com/"

def search_products_and_save():
    print("Searching products in Fake Store API and saving...", flush=True)
    try:
        resp = requests.get(URL_FAKE_STORE_API + "products")
        print(f"Response status code: {resp.status_code}", flush=True)
        if resp.status_code == 200:
            products = resp.json()
            db = SessionLocal()
            repo = ProductRepository(db)
            for it in products:
                print(f"Processing product: {it['title']}", flush=True)
                # Dica: Verifica se o produto já existe pelo nome para não duplicar
                exits = db.query(Product).filter(Product.title == it['title']).first()
                if not exits:
                    product = ProductCreate(
                        title=it['title'],
                        price=it['price'],
                        description=it['description'],
                        category=it['category'],
                        image=it['image']
                    )
                    print(product, flush=True)
                    repo.create(product)
                    print(f"Product {it['title']} saved successfully!", flush=True)
            db.close()
            print("Sync products successfully!", flush=True)
        else:
            print("Erro ao acessar a API Fake Store", flush=True)
    except Exception as e:
        print(f"Erro durante a rotina: {e}", flush=True)