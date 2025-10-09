# app/api/empresas.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate, EmpresaResponse
from app.services import empresa_service

router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)

# =========================
# ENDPOINTS EMPRESAS
# =========================

@router.get("/", response_model=List[EmpresaResponse])
def listar_empresas(db: Session = Depends(get_db)):
    """
    Lista todas las empresas activas.
    """
    empresas = empresa_service.get_empresas(db)
    return empresas


@router.get("/{empresa_id}", response_model=EmpresaResponse)
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una empresa por su ID.
    """
    empresa = empresa_service.get_empresa_by_id(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa


@router.post("/", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
def crear_empresa(empresa_in: EmpresaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva empresa (RUC debe ser único).
    """
    empresa_existente = empresa_service.get_empresa_by_ruc(db, empresa_in.ruc)
    if empresa_existente:
        raise HTTPException(status_code=400, detail="El RUC ya está registrado")

    return empresa_service.create_empresa(db, empresa_in)


@router.put("/{empresa_id}", response_model=EmpresaResponse)
def actualizar_empresa(empresa_id: int, empresa_in: EmpresaUpdate, db: Session = Depends(get_db)):
    """
    Actualiza una empresa existente.
    """
    empresa_actualizada = empresa_service.update_empresa(db, empresa_id, empresa_in)
    if not empresa_actualizada:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa_actualizada


@router.delete("/{empresa_id}", response_model=EmpresaResponse)
def eliminar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """
    Borrado lógico (marca activo='N').
    """
    empresa = empresa_service.delete_empresa(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa