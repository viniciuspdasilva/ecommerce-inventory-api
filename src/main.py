from fastapi import FastAPI

from src.infra.database import schema, Base
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.routes import router

Base.metadata.create_all(schema)

app = FastAPI(title="Inventory API MVP")

# 2. ADICIONA O CORS IMEDIATAMENTE AQUI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite o seu HTML local (porta 5500, file://, etc)
    allow_credentials=True,
    allow_methods=["*"], # Fundamental para permitir GET, POST, PUT, DELETE e OPTIONS
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "API de Estoque Operacional. Acesse /docs para testar"}
