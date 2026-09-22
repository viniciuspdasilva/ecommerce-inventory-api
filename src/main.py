from fastapi import FastAPI

from src.infra.database import schema, Base
from src.presentation.routes import router

Base.metadata.create_all(schema)

app = FastAPI(title="Inventory API MVP")

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "API de Estoque Operacional. Acesse /docs para testar"}
