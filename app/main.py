# app/main.py
from fastapi import FastAPI
from app.api import auth, empresas, roles, usuarios 
app = FastAPI(
    title="CHEMLIQ API",
    version="0.1.0",
    description="API para el sistema CHEMLIQ"
)

# =========================
# RUTAS PRINCIPALES
# =========================
app.include_router(auth.router)
app.include_router(empresas.router)
app.include_router(roles.router)
app.include_router(usuarios.router)  

#comando para ejecutar main --- uvicorn app.main:app --reload