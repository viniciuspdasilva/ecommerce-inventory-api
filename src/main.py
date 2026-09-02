from contextlib import asynccontextmanager
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from src.infra.database import schema, Base
from src.infra.tasks import search_products_and_save
from src.presentation.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Sincronizacao inicial...")
    try:
        search_products_and_save()
    except Exception as e:
        print(f"Erro ao sincronizar produtos: {e}")

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        search_products_and_save,
        'interval',
        days=1
    )
    scheduler.start()
    yield
    scheduler.shutdown()


Base.metadata.create_all(schema)

app = FastAPI(title="Inventory API MVP")

app.include_router(router)

search_products_and_save()


@app.get("/")
def read_root():
    return {"message": "API de Estoque Operacional. Acesse /docs para testar"}
