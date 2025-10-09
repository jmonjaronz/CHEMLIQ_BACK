# app/main.py
from fastapi import FastAPI
from app.api import auth, empresas

app = FastAPI(
    title="CHEMLIQ API",
    version="0.1.0",
    description="API para el sistema CHEMLIQ"
)

app.include_router(auth.router)
app.include_router(empresas.router)

#comando para ejecutar main --- uvicorn app.main:app --reload